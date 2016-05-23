# -*- coding: utf-8 -*-
import datetime

from django.db.models import F

from api.views import redis_push_obj
from sms.models import MsgSend
from sms.serv.cmpp2error import cmpp2_id0012_error
from sms.serv.smsconfig import SmsConfig
from sms.serv.smstools import get_api_user


class SmsHandler:
    def __init__(self):
        pass

    @staticmethod
    def redis_push_status_report(msg):
        if msg.msg_user in get_api_user():
            redis_push_obj('status_report', msg.msg_user_id,
                           {'id': msg.id, 'status': msg.msg_feed_result, 'send_time': msg.msg_send_time,
                            'feed_time': msg.msg_feed_time})

    @staticmethod
    def redis_push_recv_sms(msg):
        # user=msg.msg_user
        for user in msg.msg_user.dept.dept_user_set.all():
            if user in get_api_user():
                redis_push_obj('recv_sms', user.id, {'dest_id': msg.dest_id, 'src_terminal_id': msg.src_terminal_id,
                                                     'msg_content': msg.msg_content,
                                                     'msg_recv_time': msg.msg_recv_time})

    @staticmethod
    def sms_send(msg, cfg):
        msg.msg_send_time = datetime.datetime.now()
        msg.msg_stat = 'send'
        msg.channle_cfg = cfg
        msg.save()

        task = msg.msg_task
        task.submit = F('submit') + 1

        task.LastAccess = datetime.datetime.now()
        task.save()

    @staticmethod
    def sms_ack(msg, cfg, ack_result, ack_time):
        msg.msg_ack_result = ack_result
        msg.msg_ack_time = ack_time
        if msg.msg_ack_result == SmsConfig.channle_list.get(cfg).get('ack_success'):
            msg.msg_stat = 'ack.success'
        else:
            msg.msg_stat = 'ack.failed'
        if msg.msg_send_time is None:
            msg.msg_send_time = msg.msg_ack_time
        msg.channle_cfg = cfg
        msg.save()

        task = msg.msg_task
        task.submit = F('submit') + 1

        if msg.msg_stat == 'ack.failed':
            task.error = F('error') + 1
        else:
            if SmsConfig.channle_list.get(cfg).get('feed_default'):
                task.success = F('success') + 1

        task.LastAccess = datetime.datetime.now()
        task.save()

    @staticmethod
    def sms_feed(msg, cfg, feed_result, feed_time):
        if cfg == 'cmpp2cfg' and feed_result == 'ID:0012':
            cmpp2_id0012_error(msg)
            return

        msg = MsgSend.objects.get(id=msg.id)
        assert msg.msg_feed_result == None
        assert msg.msg_feed_time == None
        assert msg.msg_stat not in ('feed', 'feed.success', 'feed.failed')

        msg.msg_feed_result = feed_result
        msg.msg_feed_time = feed_time
        if msg.msg_feed_result == SmsConfig.channle_list.get(cfg).get('feed_success'):
            msg.msg_stat = 'feed.success'
        else:
            msg.msg_stat = 'feed.failed'
        msg.channle_cfg = cfg
        msg.save()

        SmsHandler.redis_push_status_report(msg)

        task = msg.msg_task
        if msg.msg_stat == 'feed.success':
            task.success = F('success') + 1
        else:
            task.error = F('error') + 1
        task.LastAccess = datetime.datetime.now()
        task.save()

    @staticmethod
    def sms_recv(msg, cfg):
        SmsHandler.redis_push_recv_sms(msg)
