# -*- coding: utf-8 -*-
from sms.models import QtppSend
import sms.serv.smstools


class QtppSendTask(sms.serv.smstools.CommonSendTask):
    def get_chnnal_name(self):
        return 'qtppcfg'


class QtppSendTaskLoadHandler(sms.serv.smstools.CommonSendTaskLoadHandler):
    def get_chnnal_name(self):
        return 'qtppcfg'

    def get_msg_obj_list(self, msg_obj):
        return self.get_qtpp_send_list(msg_obj)

    def get_qtpp_send_list(self, msg_obj):
        user = msg_obj.msg_user
        qtppcfg = self.get_channle(user)
        qtppsend = QtppSend()
        qtppsend.si_code = qtppcfg.qtpp_si_code
        qtppsend.service_code = qtppcfg.qtpp_service_code
        qtppsend.ec_code = qtppcfg.qtpp_ec_code
        qtppsend.ser_code = qtppcfg.qtpp_ser_code
        qtppsend.mobile = msg_obj.dest_terminal_id
        qtppsend.content = msg_obj.msg_content
        qtppsend.sms_msg = msg_obj
        qtppsend.sms_task = msg_obj.msg_task
        qtppsend.sms_user = msg_obj.msg_user
        return [qtppsend]
