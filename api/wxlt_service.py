# -*- coding: utf-8 -*-
from base64 import b64encode, b64decode
import urllib
import xml.etree.ElementTree as ET
from django.http import HttpResponse

from spyne.application import Application
from spyne.decorator import rpc
from spyne.service import ServiceBase
from spyne.model.primitive import Unicode
from spyne.protocol.soap import Soap11

from pyDes import triple_des, CBC, PAD_PKCS5

from X.tools import lazy_loader_const, log
from sms.views import get_task, send_task_prepare_sync
from api.views import redis_pop_obj
from api.models import WxltConfig
from X.tools.model import get_object


@lazy_loader_const
def get_wxlt_config(pinid):
    wxlt_config = get_object(WxltConfig, pinid=pinid)
    return wxlt_config and {
        'pinid': wxlt_config.pinid.encode(),
        'accountid': wxlt_config.accountid.encode(),
        'accountpwd': wxlt_config.accountpwd.encode(),
        'des_key': wxlt_config.des_key.encode(),
        'user_id': wxlt_config.dept_user_id,
    } or {}


class WxltTools:
    def __init__(self):
        pass

    @staticmethod
    def login(pinid, accountid, accountpwd):
        cfg = get_wxlt_config(pinid)
        if cfg and cfg.get('accountid') == accountid and cfg.get('accountpwd') == accountpwd:
            return cfg.get('user_id')
        return None

    @staticmethod
    def decrypt(data, pinid):
        key = get_wxlt_config(pinid).get('des_key')
        if len(key) < 24: key += ' ' * (24 - len(key))
        if len(key) > 24: key = key[:24]
        vi = '12345678'
        data = b64decode(data)
        k = triple_des(key, CBC, vi, pad=None, padmode=PAD_PKCS5)
        d = k.decrypt(data)
        return d

    @staticmethod
    def encrypt(data, pinid):
        key = get_wxlt_config(pinid).get('des_key')
        if key:
            if len(key) < 24: key += ' ' * (24 - len(key))
            if len(key) > 24: key = key[:24]
            vi = '12345678'
            k = triple_des(key, CBC, vi, pad=None, padmode=PAD_PKCS5)
            d = k.encrypt(data)
            rst = b64encode(d)
        else:
            rst = data
        return rst

    @staticmethod
    def parse_req_xml_head(xml_str):
        root = ET.fromstring(xml_str)
        pinid = root.find('Head/PINID').text
        accountid = root.find('Head/AccountId').text
        accountpwd = root.find('Head/AccountPwd').text
        user_id = WxltTools.login(pinid, accountid, accountpwd)
        return [root, pinid, user_id]

    @staticmethod
    def parse_send_req_xml(xml_str):
        root, pinid, user_id = WxltTools.parse_req_xml_head(xml_str)

        if user_id:
            body_txt = root.find('Body').text
            body_txt = WxltTools.decrypt(body_txt, pinid)
            try:
                body_xml = '<root>' + body_txt + '</root>'
                body_root = ET.fromstring(body_xml)
                Mobiles = body_root.find('Mobiles').text
                Content = body_root.find('Content').text
            except:
                Mobiles = Content = None
        else:
            Mobiles = Content = None
        return [pinid, user_id, Mobiles, Content]

    @staticmethod
    def gen_send_rsp_xml(pinid, result, msg_list):
        rsp_xml = '<Root><Result>%s</Result>%s</Root>' % (result,
                                                          ''.join(['<Msg><Mobile>%s</Mobile><Id>%s</Id></Msg>' % (
                                                              msg.get('mobile'), msg.get('id')) for msg in msg_list])
                                                          )
        rsp_xml = WxltTools.encrypt(rsp_xml, pinid)
        return rsp_xml

    @staticmethod
    def gen_rpt_rsp_xml(pinid, result, msg_list):
        rsp_xml = '<Root><Result>%s</Result>%s</Root>' % (
            result, ''.join(
                ['<Msg><Id>%s</Id><Status>%s</Status><SendTime>%s</SendTime><RecvTime>%s</RecvTime></Msg>' % (
                    msg.get('id'), msg.get('status').encode(),
                    msg.get('send_time').strftime('%Y%m%d%H%M%S'),
                    msg.get('feed_time').strftime('%Y%m%d%H%M%S'))
                 for
                 msg in msg_list])
        )
        rsp_xml = WxltTools.encrypt(rsp_xml, pinid)
        return rsp_xml

    @staticmethod
    def gen_recv_rsp_xml(pinid, result, msg_list):
        rsp_xml = '<Root><Result>%s</Result>%s</Root>' % (
            result, ''.join(
                ['<Msg><Mobile>%s</Mobile><Content>%s</Content><TunnelId>%s</TunnelId><SendTime>%s</SendTime></Msg>' % (
                    msg.get('src_terminal_id').encode(),
                    msg.get('msg_content').encode('utf8'),
                    msg.get('dest_id').encode(),
                    msg.get('msg_recv_time').strftime(
                        '%Y%m%d%H%M%S'))
                 for msg in msg_list]))
        rsp_xml = WxltTools.encrypt(rsp_xml, pinid)
        return rsp_xml


class WxltService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def echo(self, name):
        print name
        return name

    @rpc(Unicode, _returns=Unicode)
    def smsSend(self, smsSendRequest):
        log(
            title='WXLT_SERVICE_SMS_SEND_REQUEST:%s' % (smsSendRequest),
            content=None,
            logger='spyne.application',
            level='debug'
        )
        pinid, user_id, Mobiles, Content = WxltTools.parse_send_req_xml(smsSendRequest)
        smsSendResponse = ''
        if user_id:
            if Content and Mobiles:
                uid = user_id
                j_task = {
                    'type': 'default',
                    'name': 'API',
                    'priority': 3,
                    'content': Content,
                    'phones': Mobiles,
                }
                task = get_task(j_task)
                task.user_id = uid
                task.save()
                taskcount, id_list = send_task_prepare_sync(task)

                mobile_list = Mobiles.split(',')
                smsSendResponse = WxltTools.gen_send_rsp_xml(pinid, '0000',
                                                             [{'id': id_list[i], 'mobile': mobile_list[i]} for i in
                                                              range(min(len(id_list), len(mobile_list)))])
            else:
                smsSendResponse = WxltTools.gen_send_rsp_xml(pinid, '0001', [])
        else:
            smsSendResponse = WxltTools.gen_send_rsp_xml(pinid, '0002', [])

        log(
            title='WXLT_SERVICE_SMS_SEND_RESOONSE:%s' % (smsSendResponse),
            content=None,
            logger='spyne.application',
            level='debug'
        )
        return smsSendResponse

    @rpc(Unicode, _returns=Unicode)
    def smsGetReport(self, smsGetReportRequest):
        log(
            title='WXLT_SERVICE_SMS_GET_REPORT_REQUEST:%s' % (smsGetReportRequest),
            content=None,
            logger='spyne.application',
            level='debug'
        )
        root, pinid, user_id = WxltTools.parse_req_xml_head(smsGetReportRequest)
        smsGetReportResponse = ''
        if user_id:
            uid = user_id
            sms_list = []
            for i in range(100):
                msg = redis_pop_obj('status_report', uid)
                if msg is None:
                    break
                else:
                    sms_list.append(msg)
            smsGetReportResponse = WxltTools.gen_rpt_rsp_xml(pinid, '0000', sms_list)
        else:
            smsGetReportResponse = WxltTools.gen_send_rsp_xml(pinid, '0002', [])
        log(
            title='WXLT_SERVICE_SMS_GET_REPORT_RESPONSE:%s' % (smsGetReportResponse),
            content=None,
            logger='spyne.application',
            level='debug'
        )
        return smsGetReportResponse

    @rpc(Unicode, _returns=Unicode)
    def smsReceive(self, smsReceiveRequest):
        log(
            title='WXLT_SERVICE_SMS_RECEIVE_REQUEST:%s' % (smsReceiveRequest),
            content=None,
            logger='spyne.application',
            level='debug'
        )
        root, pinid, user_id = WxltTools.parse_req_xml_head(smsReceiveRequest)
        smsReceiveResponse = ''
        if user_id:
            uid = user_id
            sms_list = []
            for i in range(100):
                msg = redis_pop_obj('recv_sms', uid)
                if msg is None:
                    break
                else:
                    sms_list.append(msg)
            smsReceiveResponse = WxltTools.gen_recv_rsp_xml(pinid, '0000', sms_list)
        else:
            smsReceiveResponse = WxltTools.gen_recv_rsp_xml(pinid, '0002', [])
        log(
            title='WXLT_SERVICE_SMS_RECEIVE_RESPONSE:%s' % (smsReceiveResponse),
            content=None,
            logger='spyne.application',
            level='debug'
        )
        return smsReceiveResponse


application = Application([WxltService],
                          # tns='spyne.examples.hello',
                          tns='wxlt.api.mas.sjz.cmcc.com',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )
