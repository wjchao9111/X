# -*- coding: utf-8 -*-
import datetime
from Queue import PriorityQueue

from django.db import transaction, connection

from django.db.models import Max, Q

from X.tools.task import thread_worker_task, gevent_task, sleep
from X.tools.model import keep_db_alive
from X.tools.exception import sms_exception
from X.tools import load_cls, lazy_loader_const, log
import sms.models
from base.models import User
from sms.models import SendTask, CarrierSection
from sms.serv.smsconfig import SmsConfig


class CustManager:
    def __init__(self):
        pass

    cust_list = {}


@lazy_loader_const
def get_api_user():
    return User.objects.filter(role__perm__code='sms.api')


@lazy_loader_const
def get_user_channle_cfg(user):  # return value is {'cmpp2cfg':cmpp2cfg}
    cust_dept = user.dept.root
    client_list = CustManager.cust_list.get(cust_dept, {})
    channle_list = {}
    for channle_name in SmsConfig.channle_list.keys():
        try:
            channle_cfg = getattr(user.dept.root, channle_name)
            if client_list.get(channle_name):
                channle_list[channle_name] = channle_cfg
        except:
            # log("SMS_GET_USER_CHANNLE_CFG_ERROR", content=user, logger='sms', level='error')
            pass
    return channle_list


@lazy_loader_const
def get_carrier_section(carrier):
    return [cs.section for cs in CarrierSection.objects.filter(carrier=carrier)]


class SendTaskQueue:
    def __init__(self):
        self.queue = PriorityQueue()

    def put_task(self, task):
        self.queue.put(task)

    @sms_exception
    def fetch_sms(self, count=100):
        msg_list = []
        qsize = self.queue.qsize()
        for _ in range(qsize):
            task = self.queue.get()  # task is instance of SimpleSendTask or CommonSendTask
            try:
                ms = task.fetch_sms(count)
                if len(ms) > 0:
                    msg_list += ms
                    count -= len(ms)
                if task.get_size() > 0:
                    self.queue.put(task)
            except:
                log("SMS_SEND_TASK_FETCH_SMS_ERROR", content=task.__dict__, logger='sms', level='error')
                if not SendTaskClear.all_done(task.task):
                    self.queue.put(task)
            if count <= 0:
                break
        return msg_list


class CommonSendTask:
    def __init__(self, task, fetch_size=100):
        self.task = task
        self.fetch_size = fetch_size
        self.msg_list = []
        self.reset_fetch_status()
        self.task_left = self.get_task_count()

    def get_chnnal_name(self):
        return None

    def get_query_object(self):
        return getattr(self.task, '%s_set' % (SmsConfig.channle_list.get(self.get_chnnal_name()).get('table_name')))

    def get_task_count(self):
        return self.get_query_object().filter(sms_stat='init').count()

    def reset_fetch_status(self):
        self.get_query_object().filter(sms_stat='fetch').update(sms_stat='init')

    def fetch_sms(self, count):
        log("TASK_FETCH_SMS", content=self.task, logger='task', level='debug')
        if len(self.msg_list) < count:
            self.fetch()
        msg_list, self.msg_list = self.msg_list[:count], self.msg_list[count:]
        log("TASK_FETCH_RESULT", content=[self.task, self.task.stat, self.task_left, msg_list, self.msg_list],
            logger='task', level='debug')
        return msg_list

    @keep_db_alive
    def fetch(self):
        query = self.get_query_object().filter(sms_stat='init')[:self.fetch_size]
        msg_list = [msg_obj for msg_obj in query]
        self.get_query_object().filter(id__in=[msg_obj.id for msg_obj in msg_list]).update(sms_stat='fetch')
        self.task_left -= len(msg_list)
        if self.task_left <= 0 or len(msg_list) <= 0:
            self.task_left = self.get_task_count()
        self.msg_list += msg_list

    def get_size(self):
        return len(self.msg_list) + self.task_left

    STAT_NORMAL = 0
    STAT_PAUSE = 1
    STAT_STOP = 2

    def __cmp__(self, other):
        return cmp(self.task.priority, other.task.priority)


class SimpleSendTask:
    '''necessary member:sendTask,fetch_sms(),get_size(),__cmp__()'''

    def __init__(self, task, msg_list):
        self.task = task  # mast have sendtask
        self.msg_list = msg_list

    def fetch_sms(self, count):
        log("TASK_FETCH_SMS", content=self.task, logger='task', level='debug')
        msg_list, self.msg_list = self.msg_list[:count], self.msg_list[count:]
        log("TASK_FETCH_RESULT", content=[self.task, msg_list, self.msg_list], logger='task', level='debug')
        return msg_list

    def get_size(self):
        return len(self.msg_list)

    def __cmp__(self, other):
        return cmp(self.task.priority, other.task.priority)


class TaskRecorder:
    def __init__(self, size=10000):
        self.size = size
        self.hist = []
        self.empty_ids = []
        self.max = 0

    def record(self, ids):
        for id in ids:
            self.max = max(self.max, id)
        del_ids = []
        for id in self.hist:
            if id <= self.max - self.size:
                del_ids.append(id)
        for id in del_ids:
            self.hist.remove(id)
        self.hist += ids

    def nosee(self, id):
        return id not in self.hist

    def get_last_id(self):
        return self.max - self.size

    def get_put_list(self, task_list):
        put_list = []
        empty_ids = []
        for task in task_list:
            if task.id > self.max or self.nosee(task.id) or task.id in self.empty_ids:
                if task.count == -1:
                    self.empty_ids.append(task.id)
                else:
                    put_list.append(task)
        self.record([task.id for task in put_list])
        self.empty_ids = empty_ids
        return put_list


class CommonSendTaskLoader:
    def __init__(self, bulk_size=100):
        self.recorder = TaskRecorder()
        self.last_init_id = 0
        self.bulk_size = bulk_size
        self.cust_list = self.get_cust_list()

    def get_cust_list(self):
        return CustManager.cust_list

    def get_cust_channle_instance(self, cust, channle_name):
        try:
            inst_list = self.cust_list.get(cust)
            inst = inst_list.get(channle_name)
            return inst
        except:
            log("SMS_GET_CUST_CHANNLE_INSTANCE_ERROR", content=[cust, channle_name], logger='sms', level='error')
            return None
    
    
    @keep_db_alive
    def fetch_new_task(self):  # 使用http://redis.io/
        task_list = SendTask.objects.filter(
            Q(Q(
                id__gt=self.recorder.get_last_id(),
                stat__in=('init', 'pre.end', 'send.start'),
                user__dept__root__in=self.cust_list
            ) & ~Q(id__in=self.recorder.hist)) | Q(
                id__in=self.recorder.empty_ids
            )
        )
        put_list = self.recorder.get_put_list(task_list)
        if task_list:
            print 'fetch new task', task_list
        if put_list:
            print 'put new task', put_list

        self.put_task_list(put_list)

    def put_task_list(self, task_list):
        for task in task_list:
            self.put_task_later(task)

    @gevent_task
    def put_task_later(self, task):
        now = datetime.datetime.now()
        delay = 0
        if task.timing and task.timing > now:
            delay = (task.timing - now).total_seconds()

        if delay:
            sleep(delay)
        self.put_task(task)

    @thread_worker_task
    @keep_db_alive
    def put_task(self, task):
        log("TASK_PUT_TASK", content=task, logger='task', level='debug')
        if task.stat in ('pre.end', 'send.start'):
            if task.stat == 'pre.end':
                with transaction.atomic():
                    handler_list = self.load_task(task)
                    task.stat = 'send.start'
                    task.save()
            else:
                handler_list = self.get_load_handler(task)
            for handler in handler_list:
                channle_name = handler.get_chnnal_name()
                channle_inst = self.get_cust_channle_instance(task.user.dept.root, channle_name)
                if channle_inst is not None:
                    # new task and count<bulk_size
                    if handler.sms_count > 0 and handler.sms_count == len(handler.sms_list):
                        send_task = SimpleSendTask(task, handler.sms_list)
                    else:
                        send_task = handler.get_task_class()(task)
                    if send_task.get_size():
                        self.put_queue(channle_inst, send_task)

    def put_queue(self, channle_inst, send_task):
        log("TASK_PUT_QUEUE", content=send_task.task, logger='task', level='debug')
        channle_inst.task_queue.put_task(send_task)

    def load_task(self, task):
        handler_list = self.get_load_handler(task)
        unload_count = 0
        for msg_obj in task.msgsend_set.all():
            sms_obj_list = None
            for handler in handler_list:
                sms_obj_list = handler.load(msg_obj)
                if sms_obj_list:
                    break
            if not sms_obj_list:
                unload_count += 1
        if unload_count:
            task.error += unload_count
            task.save()
        for handler in handler_list:
            handler.close()
        none_empty_list = []
        for handler in handler_list:
            if handler.sms_count > 0:
                none_empty_list.append(handler)
        return none_empty_list

    def get_load_handler(self, task):
        handler_list = []
        user = task.user
        channle_list = get_user_channle_cfg(user)
        for channle_name in SmsConfig.channle_list.keys():
            if channle_list.get(channle_name):
                handler_list.append(load_cls(SmsConfig.channle_list.get(channle_name).get('load_handler'))())
        return handler_list


class CommonSendTaskLoadHandler:
    def __init__(self, bulk_size=100, tiny_size=10):
        self.bulk_size = bulk_size
        self.tiny_size = tiny_size
        self.sms_count = 0
        self.sms_list = []

    def get_chnnal_name(self):
        return None

    def get_msg_obj_list(self, msg_obj):
        return []

    def get_model(self):
        return load_cls(SmsConfig.channle_list.get(self.get_chnnal_name()).get('model'))

    def get_carrier(self):
        return SmsConfig.channle_list.get(self.get_chnnal_name()).get('carrier')

    def get_task_class(self):
        return load_cls(SmsConfig.channle_list.get(self.get_chnnal_name()).get('send_task'))

    def get_section(self):
        carrier_list = self.get_carrier()
        section_list = []
        for carrier in carrier_list:
            section_list += get_carrier_section(carrier)
        return section_list

    def get_channle(self, user):
        return get_user_channle_cfg(user).get(self.get_chnnal_name())

    def in_section(self, dest_id):
        for section in self.get_section():
            if dest_id.startswith(section):
                return True
        return False

    def get_sms_list(self, msg_obj):
        if self.in_section(msg_obj.dest_terminal_id):
            return self.get_msg_obj_list(msg_obj)
        else:
            return []

    def load(self, msg_obj):
        sms_obj_list = self.get_sms_list(msg_obj)
        self.sms_list += sms_obj_list
        self.sms_count += len(sms_obj_list)
        if len(self.sms_list) >= self.bulk_size:
            self.get_model().objects.bulk_create(self.sms_list[:self.bulk_size])
            self.sms_list = self.sms_list[self.bulk_size:]
        return sms_obj_list

    def close(self):
        if len(self.sms_list) > 0:
            if self.sms_count == len(self.sms_list) and self.sms_count <= self.tiny_size:
                for sms in self.sms_list:
                    sms.save()
            else:
                self.get_model().objects.bulk_create(self.sms_list)
                self.sms_count = []


class SendTaskClear:
    def __init__(self):
        pass

    @staticmethod
    @sms_exception
    def clear_all_quick():
        task_list = []
        for task in SendTask.objects.filter(stat__in=['pre.end', 'send.start', 'send.end']):
            if SendTaskClear.all_done(task):
                task_list.append(task)
        if task_list:
            SendTaskClear.task_save_quick(task_list)
        return task_list

    @staticmethod
    def all_done(task):
        expired_day = 1
        now = datetime.datetime.now()
        if ((task.success + task.error >= task.count) or
                (task.submit >= task.count and (now - task.access).days >= expired_day) or
                ((now - max(task.timing and task.timing or task.init, task.access)).days >= expired_day)
            ):
            task.stat = 'send.end'
            task.save()
            return True

    @staticmethod
    @transaction.atomic
    def task_save_quick(task_list):
        if not task_list: return
        id_list = [str(task.id) for task in task_list]
        str_id_list = ','.join(id_list)
        task = task_list[-1]
        cursor = connection.cursor()
        field_list = 'id,type,name,stat,pause,init,timing,ending,suffix,priority,content,phones,file,user_id,count,error,submit,success,groups,access'
        cursor.execute('insert into sms_sendtask%02d (%s) select %s from sms_sendtask where id in (%s)' % (
            task.access.month, field_list, field_list, str_id_list))
        field_list = 'id,registered_delivery,valid_time,at_time,src_id,dest_terminal_id,channle_cfg,msg_content,msg_count,msg_init_time,msg_send_time,msg_ack_time,msg_ack_result,msg_feed_time,msg_feed_result,msg_stat,msg_task_id,msg_user_id,msg_variable'
        cursor.execute('insert into sms_msgsend%02d (%s) select %s from sms_msgsend where msg_task_id in (%s)' % (
            task.access.month, field_list, field_list, str_id_list))

        channle_keys = SmsConfig.channle_list.keys()
        for channle_name in channle_keys:
            cursor.execute('insert into sms_%s%02d (%s) select %s from sms_%s where sms_task_id in (%s)' % (
                SmsConfig.channle_list.get(channle_name).get('table_name'),
                task.access.month,
                SmsConfig.channle_list.get(channle_name).get('field_list'),
                SmsConfig.channle_list.get(channle_name).get('field_list'),
                SmsConfig.channle_list.get(channle_name).get('table_name'),
                str_id_list))

        channle_keys.reverse()
        for channle_name in channle_keys:
            cursor.execute('delete from sms_%s where sms_task_id in (%s)' % (
                SmsConfig.channle_list.get(channle_name).get('table_name'),
                str_id_list))

        cursor.execute('delete from sms_msgsend where msg_task_id in (%s)' % str_id_list)
        cursor.execute('delete from sms_sendtask where id in (%s)' % str_id_list)

        # transaction.commit_unless_managed()

    @staticmethod
    @sms_exception
    @transaction.atomic
    def set_max_id():
        send_task_id = max(
            sms.models.SendTask.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask01.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask02.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask04.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask05.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask06.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask07.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask08.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask09.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask10.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask11.objects.aggregate(Max('id')).get('id__max'),
            sms.models.SendTask12.objects.aggregate(Max('id')).get('id__max'),
            0,
        ) + 1
        msg_send_id = max(
            sms.models.MsgSend.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend01.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend02.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend03.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend04.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend05.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend06.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend07.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend08.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend09.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend10.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend11.objects.aggregate(Max('id')).get('id__max'),
            sms.models.MsgSend12.objects.aggregate(Max('id')).get('id__max'),
            0,
        ) + 1

        cmpp_send_id = max(
            sms.models.Cmpp2Send.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send01.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send02.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send03.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send04.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send05.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send06.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send07.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send08.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send09.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send10.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send11.objects.aggregate(Max('id')).get('id__max'),
            sms.models.Cmpp2Send12.objects.aggregate(Max('id')).get('id__max'),
            0,
        ) + 1

        qtpp_send_id = max(
            sms.models.QtppSend.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend01.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend02.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend03.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend04.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend05.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend06.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend07.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend08.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend09.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend10.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend11.objects.aggregate(Max('id')).get('id__max'),
            sms.models.QtppSend12.objects.aggregate(Max('id')).get('id__max'),
            0,
        ) + 1

        cursor = connection.cursor()
        cursor.execute('ALTER TABLE sms_sendtask auto_increment=%d' % send_task_id)
        cursor.execute('ALTER TABLE sms_msgsend auto_increment=%d' % msg_send_id)
        cursor.execute('ALTER TABLE sms_cmpp2send auto_increment=%d' % cmpp_send_id)
        cursor.execute('ALTER TABLE sms_qtppsend auto_increment=%d' % qtpp_send_id)
        # transaction.commit_unless_managed()

    @staticmethod
    @sms_exception
    def clear_all_force():
        task_list = []
        for task in SendTask.objects.all():
            task_list.append(task)
        if task_list:
            SendTaskClear.task_save_quick(task_list)
        return task_list


class MessageSquence:
    def __init__(self, bit=32):
        self.sequence_Id = 0
        self.bit = bit

    def reset(self):
        self.sequence_Id = 0

    def get_next(self):
        self.sequence_Id = (self.sequence_Id + 1) % (1 << self.bit)
        return self.sequence_Id % (1 << self.bit)
