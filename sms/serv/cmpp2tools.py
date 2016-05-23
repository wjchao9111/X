# -*- coding: utf-8 -*-
import struct
import copy

import sms.serv.smstools
from sms.models import Cmpp2Send


class Cmpp2SendTask(sms.serv.smstools.CommonSendTask):
    def get_chnnal_name(self):
        return 'cmpp2cfg'


class Cmpp2SendTaskLoadHandler(sms.serv.smstools.CommonSendTaskLoadHandler):
    def get_chnnal_name(self):
        return 'cmpp2cfg'

    def get_msg_obj_list(self, msg_obj):
        return self.get_cmpp2send_list(msg_obj)

    def get_cmpp2send_list(self, msg_obj):
        user = msg_obj.msg_user
        cmpp2cfg = self.get_channle(user)
        cmpp2send = Cmpp2Send()
        cmpp2send.msg_src = cmpp2cfg.cmpp_sp_id
        cmpp2send.service_id = cmpp2cfg.cmpp_service_id
        cmpp2send.src_id = cmpp2cfg.cmpp_src_id + msg_obj.src_id
        cmpp2send.dest_terminal_id = msg_obj.dest_terminal_id
        cmpp2send.msg_content = msg_obj.msg_content
        cmpp2send.registered_delivery = msg_obj.registered_delivery
        cmpp2send.destUsr_tl = len(cmpp2send.dest_terminal_id.split(','))
        cmpp2send.sms_msg = msg_obj
        cmpp2send.sms_task = msg_obj.msg_task
        cmpp2send.sms_user = msg_obj.msg_user
        cmpp2send.valid_time = msg_obj.valid_time
        cmpp2send.at_time = msg_obj.at_time
        msg_content = cmpp2send.msg_content.encode(cmpp2cfg.get_cmpp_msg_fmt_display())
        cmpp2send.msg_length = len(msg_content)
        cmpp2send.msg_fmt = cmpp2cfg.cmpp_msg_fmt

        sign_zh = cmpp2cfg.cmpp_sign_zh.encode(cmpp2cfg.get_cmpp_msg_fmt_display())
        msg_content_list = self.content_split(msg_content, sign_zh, cmpp2cfg.get_cmpp_msg_fmt_display())
        if len(msg_content_list) <= 1:
            return [cmpp2send]
        else:
            sms_list = []
            msg_id = self.get_msg_id()
            for i in range(len(msg_content_list)):
                msg_content = msg_content_list[i]
                msg_content = struct.pack('!6B' + str(len(msg_content)) + 's',
                                          5, 0, 3, msg_id, len(msg_content_list), i + 1, msg_content
                                          )
                sms_obj = copy.copy(cmpp2send)
                sms_obj.pk_total = len(msg_content_list)
                sms_obj.pk_number = i + 1
                sms_obj.msg_content = msg_content.decode(cmpp2cfg.get_cmpp_msg_fmt_display())
                sms_obj.msg_length = len(msg_content)
                sms_obj.tp_udhi = 1
                sms_list.append(sms_obj)
            return sms_list

    def content_split(self, msg_content, sign_zh, charset):
        sign_zh_length = len(sign_zh) + 4
        total_length = len(msg_content)
        if total_length + sign_zh_length <= 140:
            return [msg_content]
        else:
            msg_content_list = []
            while len(msg_content) > 0:
                if total_length != len(msg_content):
                    sign_zh_length = 0
                length = 134 - sign_zh_length
                try:
                    msg_content[:length].decode(charset)
                except:
                    length -= 1

                msg_content_list += [msg_content[:length], ]
                msg_content = msg_content[length:]
            return msg_content_list

    def get_msg_id(self):
        return MsgIDSquence.get_next()


class MsgIDSquence:
    def __init__(self):
        pass

    sequence_Id = 0
    bit = 7

    @staticmethod
    def reset():
        sequence_Id = 0

    @staticmethod
    def get_next():
        sequence_Id = (MsgIDSquence.sequence_Id + 1) % (1 << MsgIDSquence.bit)
        return MsgIDSquence.sequence_Id % (1 << MsgIDSquence.bit)
