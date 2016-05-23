# -*- coding: utf-8 -*-


class SmsConfig:
    def __init__(self):
        pass

    channle_list = {
        'cmpp2cfg': {
            'name': u'网内短信',
            'carrier': ['CM'],
            'model': 'sms.models.Cmpp2Send',
            'table_name': 'cmpp2send',
            'field_list': 'id,msg_id,pk_total,pk_number,registered_delivery,msg_level,service_id,fee_userType,fee_terminal_Id,tp_pId,tp_udhi,msg_fmt,msg_src,feetype,feecode,valid_time,at_time,src_id,destUsr_tl,dest_terminal_id,msg_length,msg_content,reserve,sms_init_time,sms_send_time,sms_ack_time,sms_ack_result,sms_done_time,sms_feed_time,sms_feed_result,sms_stat,sms_msg_id,sms_task_id,sms_user_id',
            'status_field': 'cmpp_status',
            'client': 'sms.serv.cmpp2client.Cmpp2Client',
            'send_task': 'sms.serv.cmpp2tools.Cmpp2SendTask',
            'load_handler': 'sms.serv.cmpp2tools.Cmpp2SendTaskLoadHandler',
            'ack_success': '0',
            'feed_success': 'DELIVRD',
            'feed_default': None,
        },
        'qtppcfg': {
            'name': u'全通异网',
            'carrier': ['CU', 'CT'],
            'model': 'sms.models.QtppSend',
            'table_name': 'qtppsend',
            'field_list': 'id,msg_id,si_code,service_code,ec_code,fun_code,ser_code,src_id,mobile,content,msg_length,sms_init_time,sms_send_time,sms_ack_time,sms_ack_result,sms_done_time,sms_feed_time,sms_feed_result,sms_stat,sms_msg_id,sms_task_id,sms_user_id',
            'status_field': 'qtpp_status',
            'client': 'sms.serv.qtppclient.QtppClient',
            'send_task': 'sms.serv.qtpptools.QtppSendTask',
            'load_handler': 'sms.serv.qtpptools.QtppSendTaskLoadHandler',
            'ack_success': '1000',
            'feed_success': 'DELIVRD',
            'feed_default': 'DELIVRD',
        },
    }

    last_cfg = 'qtppcfg'

    sleep_time = (20, 8)
