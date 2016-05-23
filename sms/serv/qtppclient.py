# -*- coding: utf-8 -*-
import random
import xml.etree.ElementTree as ET
import datetime
from xml.sax.saxutils import escape

from suds.client import Client
import gevent.monkey

from X.tools.exception import sms_exception
from X.tools.log import log
import sms.serv.smstools
from sms.serv.qtpphandler import QtppHandler
from X.tools.task import sleep, gevent_task


class QtppClient:
    def __init__(self, config):
        gevent.monkey.patch_socket()
        self.config = config
        self.handler = QtppHandler()
        self.status = None
        self.fetch_size = 10
        self.fetch_interval = 1
        self.task_queue = sms.serv.smstools.SendTaskQueue()

    @gevent_task
    def start_serv(self):
        self.status = 'running'
        while self.status:
            try:
                client = Client(self.config.qtpp_wsdl_url.encode())
                self.sms_mt = client.service.smsMt
                break
            except:
                log(
                    title='QTPP_START_SERV_ERROR',
                    content=self.config.__dict__,
                    logger='sms',
                    level='error'
                )

        while self.status:
            sms_list = self.task_queue.fetch_sms(self.fetch_size)
            if sms_list:
                for sms in sms_list:
                    self.send_one(sms)
            else:
                sleep(self.fetch_interval)

    def stop_serv(self):
        self.status = None

    @sms_exception
    def send_one(self, msg):  # ack 暂时不支持群发
        mobile_list = msg.mobile.encode().split(',')
        resultcode = '-1'
        result_list = []
        try:
            req_xml = self.get_req_xml(msg)
            log(
                title='QTPP_SEND_REQ_XML_%s' % msg.ec_code,
                content=req_xml,
                logger='sms',
                level='debug'
            )
            rsp_xml = self.sms_mt(req_xml)
            rsp_xml = unicode(rsp_xml).encode('utf8')
            log(
                title='QTPP_SEND_RSP_XML_%s' % msg.ec_code,
                content=rsp_xml,
                logger='sms',
                level='debug'
            )
            resultcode, result_list = self.parse_rsp_xml(rsp_xml)
        except:
            log(
                title='QTPP_SEND_ERROR_%s' % msg.ec_code,
                content=None,
                logger='sms',
                level='error'
            )
        for result in result_list:
            mobile = result.get('mobile')
            mobile_list.remove(mobile)
            result['sms_obj'] = msg
            self.handler.sms_ack(self, result)
        for mobile in mobile_list:
            result = {'mobile': mobile, 'oprnum': msg.id, 'resultcode': resultcode, 'sms_obj': msg}
            self.handler.sms_ack(self, result)

    def parse_rsp_xml(self, xml_str):
        root = ET.fromstring(xml_str)
        rst_xml_list = root.findall('BODY/RESULTLIST/RESULT')
        result_list = []
        try:
            resultcode = root.find('BODY/RETCODE').text
        except:
            resultcode = -1
        for rst_xml in rst_xml_list:
            mobile = rst_xml.find('MOBILE').text
            oprnum = rst_xml.find('OPRNUM').text
            resultcode = rst_xml.find('RESULTCODE').text
            result_list.append({'mobile': mobile, 'oprnum': oprnum, 'resultcode': resultcode})
        return resultcode, result_list

    def get_req_xml(self, msg):
        si_code = msg.si_code.encode()
        sid = msg.id
        now = datetime.datetime.now()
        timestamp = '%04d%02d%02d%02d%02d%02d%03d' % (
            now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond / 1000)
        service_code = msg.service_code.encode()
        ec_code = msg.ec_code.encode()
        fun_code = msg.fun_code.encode()
        mobile = msg.mobile.encode()
        content = escape(msg.content)
        ser_code = msg.ser_code.encode()

        xml_str = '''<?xml version="1.0" encoding="UTF-8"?>
<SmsMtReq>
    <HEAD>
        <SICODE>%s</SICODE>
        <SID>%s</SID>
        <TIMESTAMP>%s</TIMESTAMP>
    </HEAD>
    <BODY>
        <SERVICECODE>%s</SERVICECODE>
        <ECCODE>%s</ECCODE>
        <FUNCODE>%s</FUNCODE>
        <MOBILE>%s</MOBILE>
        <CONTENT>%s</CONTENT>
        <SENDTIME>%s</SENDTIME>
    </BODY>
    <YWHD>
        <MESSAGEID>%s%010d</MESSAGEID>
        <SERCODE>%s</SERCODE>
        <MESSAGELEN>%s</MESSAGELEN>
    </YWHD>
</SmsMtReq>
''' % (si_code, sid, timestamp, service_code, ec_code, fun_code, mobile, content, timestamp, now.strftime('%m%d%H%M%S'),
       random.randint(0, 9999999999), ser_code, len(content))
        return xml_str
