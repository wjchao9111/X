# -*- coding: utf-8 -*-
import datetime

from django.db import transaction

from X.tools.exception import sms_exception
from sms.serv.smshandler import SmsHandler


class QtppHandler:
    def __init__(self):
        pass

    @sms_exception
    @transaction.atomic
    def sms_ack(self, channel, msg):
        sms = msg.get('sms_obj')
        # sms.msg_id=msg.get('oprnum')
        sms.sms_ack_result = msg.get('resultcode')
        sms.sms_send_time = sms.sms_ack_time = datetime.datetime.now()
        sms.sms_stat = 'ack'
        sms.save()

        sms_msg = sms.sms_msg

        SmsHandler.sms_ack(sms_msg, 'qtppcfg', sms.sms_ack_result, sms.sms_ack_time)
        return msg

    @sms_exception
    @transaction.atomic
    def sms_feed(self, channel, msg):
        # 这个函数是假的，如果处理状态报告，此函数需重写
        sms = msg.get('sms_obj')
        sms.sms_feed_result = msg.get('resultcode')
        sms.sms_feed_time = sms.sms_done_time = datetime.datetime.now()
        sms.sms_stat = 'feed'
        sms.save()

        sms_msg = sms.sms_msg

        SmsHandler.sms_feed(sms_msg, 'qtppcfg', sms.sms_feed_result, sms.sms_feed_time)

        return msg
