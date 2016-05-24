# -*- coding: utf-8 -*-
import datetime

from django.db.models import Q, F, Count, Sum
from django.shortcuts import render

from X.tools import load_cls
from X.tools.middleware import JsonResponse
from X.tools.model import get_object, object_list, auto_filter, json_success
from base.models import Dept, User
from base.verify import model_filter as base_model_filter
from sms.models import Processor, SendTask, MsgSend
from sms.serv.smsconfig import SmsConfig
from sms.tasks import send_task_prepare
from sms.verify import model_filter, model_default, model_check


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
    send_task_prepare.delay(task.id)
