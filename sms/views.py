# -*- coding: utf-8 -*-
import datetime

from django.db.models import Q, F, Count, Sum
from django.db import transaction
from django.shortcuts import render
import xlrd

from X.tools.middleware import JsonResponse
from X.tools.model import get_object, object_list, auto_filter, json_success
from X.tools.task import gevent_task,thread_task,sleep
from X.tools import load_cls, lazy_loader_const
from sms.verify import model_filter, model_default, model_check
from base.models import Dept, User
from sms.models import Processor, SendTask, MsgSend
from addr.models import AddressGroup
from sms.serv.smsconfig import SmsConfig
from base.verify import model_filter as base_model_filter
from X.tools.log import log


@object_list
def processor_list(request, pid):
    qs = Dept.objects.all()
    qs = qs.filter(
        type='company',
        stat='normal',
        root_id=F('id')
    )

    filter = None
    for cfg in SmsConfig.channle_list.keys():
        if filter is None:
            filter = Q(**{cfg + '__isnull': False})
        else:
            filter = filter | Q(**{cfg + '__isnull': False})
    qs = qs.filter(filter)

    qs = qs.filter(
        processor__pid=pid
    )
    return qs


@json_success
def processor_update(request):
    obj = request.json['object']
    dept_id = obj.get('dept_id')
    pid = obj.get('pid')

    proc = get_object(Processor, processor_dept_id=dept_id)
    if not proc:
        proc = Processor()
        proc.processor_dept_id = dept_id
    if pid is None or pid == '':
        if proc.id:
            proc.delete()
    else:
        proc.pid = pid
        proc.save()


@json_success
def processor_delete(request):
    ids = request.json['ids']
    id_list = ids.split('.')
    proc_list = Processor.objects.filter(processor_dept_id__in=id_list)
    model_check(request, proc_list)
    proc_list.delete()


@object_list
def api_user_list(request):
    qs = User.objects.filter(role__perm__code='sms.api')
    return qs


@object_list
def wxlt_user_list(request):
    qs_admin_user = base_model_filter(request, User.objects.all())
    qs_api_user = User.objects.filter(role__perm__code='sms.api')
    return User.objects.filter(id__in=[u.id for u in qs_admin_user] + [u.id for u in qs_api_user])


@object_list
@auto_filter
def task_list(request, month=0):
    model = load_cls('sms.models.SendTask')
    month = int(month)
    if month:
        model = load_cls('sms.models.SendTask%02d' % month)
    qs = model.objects.all().order_by('-id')
    return qs


def task_export(request, month, export):
    model = load_cls('sms.models.SendTask')
    month = int(month)
    if month:
        model = load_cls('sms.models.SendTask%02d' % month)
    task_list = model.objects.select_related("user").all()

    task_list = model_filter(request, task_list)
    response = render(request, 'export_sendtask.html', {'task_list': task_list})
    response['Content-Disposition'] = 'attachment; filename=%s' % 'Export.xls'
    return response


def msg_send_count(request):
    now = datetime.datetime.now()
    month = now.month
    model1 = load_cls('sms.models.MsgSend')
    model2 = load_cls('sms.models.MsgSend%02d' % month)
    now = datetime.datetime.strptime(now.strftime('%Y%m%d%H' + '0000'), '%Y%m%d%H%M%S')
    now = now + datetime.timedelta(hours=1)
    lastday = now - datetime.timedelta(hours=24)
    hour_count = [0] * 24
    for model in [model1, model2]:
        qs = model.objects.filter(msg_ack_time__lt=now, msg_ack_time__gte=lastday)
        qs = model_filter(request, qs)
        data_set = qs.extra(select={'hour': 'EXTRACT(hour from msg_ack_time)'}).values('hour').annotate((Count('id')))
        for data in data_set:
            hour_count[data['hour']] += data['id__count']
    result_set = []
    for hour in range(now.hour, 24) + range(now.hour):
        result = {'hour': str(hour), 'count': hour_count[hour]}
        result_set.append(result)
    return JsonResponse({'object_count': len(result_set), 'object_list': result_set})


@object_list
@auto_filter
def msg_send_list(request, month, task_id):
    month = int(month)
    model = load_cls('sms.models.MsgSend')
    if month:
        model = load_cls('sms.models.MsgSend%02d' % month)
    qs = model.objects.all().order_by('-id')
    task_id = int(task_id)
    if task_id: qs = qs.filter(msg_task_id=task_id)
    return qs


def msg_send_export(request, month, task_id, export):
    month = int(month)
    model = load_cls('sms.models.MsgSend')
    if month:
        model = load_cls('sms.models.MsgSend%02d' % month)
    msg_list = model.objects.select_related("msg_user").all()

    task_id = int(task_id)
    if task_id: msg_list = msg_list.filter(msg_task_id=task_id)

    msg_list = model_filter(request, msg_list)

    response = render(request, 'export_msgsend.html', {'msg_list': msg_list})
    response['Content-Disposition'] = 'attachment; filename=%s' % 'Export.xls'
    return response


def msg_send_report(request, month, task_id, report):
    month = int(month)
    model = load_cls('sms.models.MsgSend')
    if month:
        model = load_cls('sms.models.MsgSend%02d' % month)
    msg_list = model.objects.select_related("msg_user").all()

    task_id = int(task_id)
    if task_id: msg_list = msg_list.filter(msg_task_id=task_id)

    msg_list = model_filter(request, msg_list)

    data_set = msg_list.extra(
        select={'year': 'EXTRACT(year from msg_init_time)', 'month': 'EXTRACT(month from msg_init_time)',
                'day': 'EXTRACT(day from msg_init_time)'}).values('year', 'month', 'day', 'msg_user__name',
                                                                  'msg_stat', 'channle_cfg').annotate(
        (Sum('msg_count')))
    for data in data_set:
        if 'msg_stat' in data:
            msg_stat = data['msg_stat']
            for kw in MsgSend.stat_choices:
                if kw[0] == msg_stat:
                    data['msg_stat'] = kw[1]
        if 'channle_cfg' in data:
            channle_cfg = data['channle_cfg']
            if channle_cfg in SmsConfig.channle_list:
                data['channle_cfg'] = SmsConfig.channle_list[channle_cfg].get('name')

    response = render(request, 'report_msgsend.html', {'data_set': data_set})
    response['Content-Disposition'] = 'attachment; filename=%s' % 'Export.xls'
    return response


def get_task(obj):
    task = SendTask()
    if obj.get('type'): task.type = obj.get('type')
    if obj.get('name'): task.name = obj.get('name')
    if obj.get('priority'): task.priority = obj.get('priority')
    if obj.get('content'): task.content = obj.get('content')
    if obj.get('phones'): task.phones = obj.get('phones')
    if obj.get('groups'): task.groups = obj.get('groups')
    if obj.get('suffix', '') != None: task.suffix = obj.get('suffix', '')

    if obj.get('timing-date') and obj.get('timing-time'):
        year, month, day = obj.get('timing-date').split('-')
        hour, minute, second = obj.get('timing-time').split(':')
        task.timing = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    if obj.get('ending-date') and obj.get('ending-time'):
        year, month, day = obj.get('ending-date').split('-')
        hour, minute, second = obj.get('ending-time').split(':')
        task.ending = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    return task


@json_success
def task_insert(request):
    obj = request.json['object']

    task = get_task(obj)
    task.file = request.FILES.get('object.file')

    model_default(request, task)
    model_check(request, task)

    task.save()
    send_task_prepare(task)
    

class TaskLoader:
    def __init__(self, task):
        self.task = task
        self.sms_list = []
        self.sms_pos = 0
        self.sms_size = 0
        self.prepare()

    def prepare(self):
        if self.task.type in ['default', 'quick']:
            no_list = []
            no_list += self.get_no_list_from_phones()
            no_list += self.get_no_list_from_groups()
            no_list += self.get_no_list_from_file()
            self.sms_list = self.get_sms_list_from_no_list(no_list)
        if self.task.type in ['dynamic']:
            self.sms_list = self.get_sms_list_from_file()
        self.sms_size = len(self.sms_list)

    def fetch_msg(self, count):
        msg_list = []
        for i in range(count):
            if self.sms_pos < self.sms_size:
                sms = self.sms_list[self.sms_pos]
                msg = self.get_msg(sms[0], sms[1])
                msg_list.append(msg)
                self.sms_pos += 1
        return msg_list

    def get_no_list_from_phones(self):
        task = self.task
        no_list = []
        if task.phones:
            no_list += task.phones.split(',')
        return no_list

    def get_no_list_from_groups(self):
        task = self.task
        no_list = []
        if task.groups:
            grp_list = task.groups.split(',')
            for grp in AddressGroup.objects.filter(id__in=grp_list):
                no_list += [addr.phone for addr in grp.address_set.all()]
        return no_list

    def get_no_list_from_file(self):
        task = self.task
        no_list = []
        if task.file:
            book = xlrd.open_workbook(task.file.path)
            sheet = book.sheets()[0]
            rows = sheet.nrows
            cols = sheet.ncols
            for row in range(1, rows):
                row_data = sheet.row_values(row)
                if row_data:
                    phone = self.get_excel_value(row_data[0])
                    no_list.append(phone)
        return no_list

    def get_sms_list_from_file(self):
        task = self.task
        sms_list = []
        if task.file:
            book = xlrd.open_workbook(task.file.path)
            sheet = book.sheets()[0]
            rows = sheet.nrows
            cols = sheet.ncols
            key_data = sheet.row_values(0)
            key_list = []
            for col in range(cols):
                key_list.append(self.get_excel_value(key_data[col]))
            for row in range(1, rows):
                row_data = sheet.row_values(row)
                if row_data:
                    value_list = []
                    for col in range(cols):
                        value_list.append(self.get_excel_value(row_data[col]))
                    phone = self.get_excel_value(row_data[0])
                    content = self.get_msg_content(key_list, value_list)
                    sms_list.append([phone, content])
        return sms_list

    def get_sms_list_from_no_list(self, no_list):
        content = self.task.content
        return [[no, content] for no in no_list]

    def get_msg(self, phone, content=None):
        task = self.task
        if content == None:
            content = task.content
        msg = MsgSend(
            registered_delivery=task.type != 'quick' and 1 or 0,
            valid_time=task.ending,
            at_time=task.timing,
            src_id=task.suffix,
            dest_terminal_id=phone,
            msg_content=content,
            msg_user=task.user,
            msg_task=task,
        )
        msg.msg_count = get_msg_count(msg)
        return msg

    def get_excel_value(self, val):
        if type(val) == float:
            if val == int(val):
                return str(int(val))
            else:
                return val
        return val

    def get_msg_content(self, key_list, value_list):
        content = self.task.content
        for i in range(len(key_list)):
            content = content.replace('%' + key_list[i] + '%', unicode(value_list[i]))
        return content


@lazy_loader_const
def get_user_cmpp2cfg(user):
    return user.dept.root.cmpp2cfg


def get_msg_count(msg):
    u_content = msg.msg_content
    try:
        u_sign_zh = get_user_cmpp2cfg(msg.msg_user).cmpp_sign_zh
    except:
        u_sign_zh = u''
    if type(u_content) == str:
        u_content = u_content.decode('utf8')
    if type(u_sign_zh) == str:
        u_sign_zh = u_sign_zh.decode('utf8')

    u_len = len(u_content) + len(u_sign_zh) + 2
    if u_len < 70:
        return 1
    else:
        return int((u_len + 67 - 1) / 67)


def send_task_prepare_sync(task, bulk_size=100, pack_size=20):
    success = False
    try:
        with transaction.atomic():
            loader = TaskLoader(task)
            msg_count = loader.sms_size
            id_list = []
            while True:
                msg_list = loader.fetch_msg(100)
                if msg_list:
                    for msg in msg_list:
                        msg.save()
                        id_list.append(msg.id)
                else:
                    break
            task.stat = 'pre.end'
            task.count = msg_count
            task.save()
            success = True
            return msg_count, id_list
    finally:
        if not success:
            task.stat = 'pre.fail'
            task.save()


@thread_task
def send_task_prepare(task, bulk_size=100, pack_size=20):
    success = False
    try:
        with transaction.atomic():
            loader = TaskLoader(task)
            msg_count = loader.sms_size
            id_list = []
            log('SEND_TASK_PREPARE','ID:%s,MSG_COUNT_ALL:%s'%(task.id,msg_count),'file','debug')
            count_1 = 0
            while True:
                msg_list = loader.fetch_msg(100)
                if msg_list:
                    MsgSend.objects.bulk_create(msg_list)
                else:
                    break
                count_1+=len(msg_list)
                sleep(0)
                log('SEND_TASK_PREPARE','ID:%s,MSG_COUNT_DONE:%s'%(task.id,count_1),'file','debug')
            
            task.stat = 'pre.end'
            task.count = msg_count
            task.save()
            success = True
    except:
        log('SEND_TASK_PREPARE','ID:%s'%(task.id),'file','error')
        if not success:
            task.stat = 'pre.fail'
            task.save()
