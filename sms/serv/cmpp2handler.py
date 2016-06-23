# -*- coding: utf-8 -*-
import datetime
import base64

from django.db import transaction
from X.settings import debugging

from base.models import User
from sms.models import Cmpp2Send, Cmpp2Recv, MsgRecv
from X.tools.exception import sms_exception
from X.tools.log import log
from sms.serv.smshandler import SmsHandler


class Cmpp2Handler:
    def __init__(self):
        pass

    @sms_exception
    @transaction.atomic
    def sms_send(self, channel, msg):
        sms = msg.get('sms_obj')
        sms.sms_send_time = datetime.datetime.now()
        sms.sms_stat='send'
        sms.save()
        self.msg_send_update(sms.sms_msg)

    def msg_send_update(self, msg):
        sms_list = [sms for sms in msg.cmpp2send_set.order_by('sms_send_time')]
        for sms in sms_list:
            if sms.sms_send_time is None:
                return
        last_send_time = sms_list[-1].sms_send_time
        msg.msg_send_time = last_send_time
        msg.msg_stat = 'send'
        msg.save()
        SmsHandler.sms_send(msg, 'cmpp2cfg')

    @sms_exception
    @transaction.atomic
    def sms_ack(self, channel, msg):
        sms = msg.get('sms_obj')
        sms.msg_id = msg.get('msg_id')
        sms.sms_ack_result = msg.get('result')
        sms.sms_ack_time = datetime.datetime.now()
        sms.sms_stat = 'ack'
        sms.save()
        self.msg_ack_update(sms.sms_msg)
        return msg

    def merge_result(self, result_list):
        if result_list:
            result = result_list[0]
            try:
                for r in result_list:
                    assert r == result
            except:
                return '|'.join(result_list)
            else:
                return result
        else:
            return None

    def msg_ack_update(self, msg):
        sms_list = [sms for sms in msg.cmpp2send_set.order_by('sms_ack_time')]
        for sms in sms_list:
            if sms.sms_ack_time is None or sms.sms_ack_result is None:
                return
        last_ack_time = sms_list[-1].sms_ack_time
        all_ack_result = self.merge_result([sms.sms_ack_result for sms in sms_list])

        SmsHandler.sms_ack(msg, 'cmpp2cfg', all_ack_result, last_ack_time)

    @sms_exception
    @transaction.atomic
    def sms_feed(self, channel, msg):
        for sms in Cmpp2Send.objects.all().filter(
                msg_id=msg.get('msg_id')
        ):
            sms.sms_feed_result = msg.get('stat')
            sms.sms_done_time = self.get_done_time(msg.get('done_time'))
            sms.sms_feed_time = datetime.datetime.now()
            sms.sms_stat = 'feed'

            sms.save()
            self.msg_feed_update(sms.sms_msg)
        return msg

    def msg_feed_update(self, msg):
        sms_list = [sms for sms in msg.cmpp2send_set.order_by('sms_feed_time')]
        for sms in sms_list:
            if sms.sms_feed_time is None or sms.sms_feed_result is None:
                return
        last_feed_time = sms_list[-1].sms_feed_time
        all_feed_result = self.merge_result([sms.sms_feed_result for sms in sms_list])

        SmsHandler.sms_feed(msg, 'cmpp2cfg', all_feed_result, last_feed_time)

    def get_done_time(self, dt):
        if debugging:
            now = datetime.datetime.now()
            year = now.year
            done_time = datetime.datetime(
                year,
                int(dt[0:2]),
                int(dt[2:4]),
                int(dt[4:6]),
                int(dt[6:8]),
                int(dt[8:10]),
            )
        else:
            done_time=datetime.datetime.strptime(dt,'%y%m%d%H%M')
        return done_time

    @sms_exception
    @transaction.atomic
    def sms_recv(self, channle, msg):
        cmpp2 = channle
        msg['dest_id'] = self.get_string(msg['dest_id'])
        msg['service_id'] = self.get_string(msg['service_id'])
        msg['src_terminal_id'] = self.get_string(msg['src_terminal_id'])
        # msg['msg_content']=self.get_string(msg['msg_content'])
        msg['reserved'] = self.get_string(msg['reserved'])
        # print msg['dest_id']
        if msg['tp_udhi']:
            if msg['msg_content'][0] == '\5':
                msg['sms_identity'] = ord(msg['msg_content'][3])
                msg['sms_pk_total'] = ord(msg['msg_content'][4])
                msg['sms_pk_number'] = ord(msg['msg_content'][5])
                msg['msg_content'] = self.sms_decode(msg['msg_fmt'], self.get_string(msg['msg_content'][6:]))

            else:
                msg['sms_identity'] = ord(msg['msg_content'][3]) * 256 + ord(msg['msg_content'][4])
                msg['sms_pk_total'] = ord(msg['msg_content'][5])
                msg['sms_pk_number'] = ord(msg['msg_content'][6])
                msg['msg_content'] = self.sms_decode(msg['msg_fmt'], self.get_string(msg['msg_content'][7:]))

        else:
            msg['sms_identity'] = 1
            msg['sms_pk_total'] = 1
            msg['sms_pk_number'] = 1
            msg['msg_content'] = self.sms_decode(msg['msg_fmt'], msg['msg_content'])

        sms = Cmpp2Recv()
        sms.msg_id = msg.get('msg_id')
        sms.dest_id = msg.get('dest_id')
        sms.service_id = msg.get('service_id')
        sms.tp_pid = msg.get('tp_pid')
        sms.tp_udhi = msg.get('tp_udhi')
        sms.msg_fmt = msg.get('msg_fmt')
        sms.src_terminal_id = msg.get('src_terminal_id')
        sms.registered_delivery = msg.get('registered_delivery')
        sms.msg_length = msg.get('msg_length')
        sms.msg_content = msg.get('msg_content')
        sms.reserved = msg.get('reserved')

        sms.sms_identity = msg.get('sms_identity')
        sms.sms_pk_total = msg.get('sms_pk_total')
        sms.sms_pk_number = msg.get('sms_pk_number')

        dept = cmpp2.config.cmpp_dept
        cmpp_src_id = cmpp2.config.cmpp_src_id
        try:
            _, suffix = sms.dest_id.split(cmpp_src_id)
            sms.sms_user = User.objects.get(dept__root=dept, suffix=suffix)
        except:
            sms.sms_user = dept.admin_user

        sms.save()
        self.msg_recv_update(sms)
        return msg

    def msg_recv_update(self, sms):
        if sms.tp_udhi:
            sms_list = [sms_obj
                        for sms_obj in Cmpp2Recv.objects.all().filter(
                    dest_id=sms.dest_id,
                    src_terminal_id=sms.src_terminal_id,
                    sms_identity=sms.sms_identity,
                    sms_msg__isnull=True,
                ).order_by('sms_pk_number')]
            if len(sms_list) == sms.sms_pk_total:
                msg = MsgRecv()
                msg.dest_id = sms.dest_id
                msg.src_terminal_id = sms.src_terminal_id
                msg.msg_content = ''.join([sms_obj.msg_content for sms_obj in sms_list])
                msg.msg_recv_time = sms.sms_recv_time
                msg.msg_user = sms.sms_user
                msg.cmpp2send_set = sms_list
                msg.save()

                for sms in sms_list:
                    sms.sms_msg = msg
                    sms.save()
                SmsHandler.sms_recv(msg, 'cmpp2cfg')
        else:
            msg = MsgRecv()
            msg.dest_id = sms.dest_id
            msg.src_terminal_id = sms.src_terminal_id
            msg.msg_content = sms.msg_content
            msg.msg_recv_time = sms.sms_recv_time
            msg.msg_user = sms.sms_user
            msg.cmpp2send_set = [sms]
            msg.save()

            sms.sms_msg = msg
            sms.save()

            SmsHandler.sms_recv(msg, 'cmpp2cfg')

    def get_string(self, data):
        data_len = len(data)
        for i in range(data_len):
            if data[data_len - i - 1] != '\0':
                return data[:data_len - i]
        return ''

    def sms_decode(self, fmt, data):
        try:
            if fmt == 0:  # ascii
                return data.decode('ascii')
            elif fmt == 1:  # writecard
                return ''.join([len(hex(ord(c))) == 3 and '0' + hex(ord(c))[2:] or hex(ord(c))[2:] for c in data])
            elif fmt == 4:  # bin
                return ''.join([len(hex(ord(c))) == 3 and '0' + hex(ord(c))[2:] or hex(ord(c))[2:] for c in data])
            elif fmt == 8:
                return data.decode('UTF-16BE')
            elif fmt == 15:
                return data.decode('gbk')
            return data
        except:
            log(
                title='CMPP2_SMS_DECODE_%s_%s' % (fmt, base64.b64encode(data)),
                content=None,
                logger='sms',
                level='error'
            )
            return ''
