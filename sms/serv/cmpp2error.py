from sms.serv.qtpptools import QtppSendTaskLoadHandler
from sms.serv.smsconfig import SmsConfig
from sms.serv.smstools import get_user_channle_cfg, CustManager, SimpleSendTask


def cmpp2_id0012_error(msg):
    channle_name = SmsConfig.last_cfg
    channle_list = get_user_channle_cfg(msg.msg_user)
    if channle_name in SmsConfig.channle_list and channle_name in channle_list:
        channle_cfg = channle_list.get(channle_name)
        channle_inst = CustManager.cust_list.get(msg.msg_user.dept.root).get(channle_name)

        load_handler = QtppSendTaskLoadHandler()
        sms_list = load_handler.get_msg_obj_list(msg)
        for sms in sms_list:
            sms.save()
        send_task = SimpleSendTask(msg.msg_task, sms_list)
        channle_inst.task_queue.put_task(send_task)
