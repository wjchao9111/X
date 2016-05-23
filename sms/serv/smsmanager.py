# -*- coding: utf-8 -*-

from sms.serv.smsconfig import SmsConfig
from sms.serv.smstools import SendTaskClear, CustManager
from base.models import Dept
from X.tools.task import keep_interval
from X.tools.model import keep_db_alive
from X.tools import load_cls
from X.tools.task import sleep
from start_process import django_setup
from X.tools.log import log


class ChannleProcess:  # (Process):
    def __init__(self, pid, req_queue, rsp_queue, interval=10):
        # Process.__init__(self)
        self.pid = pid
        self.req_queue = req_queue
        self.rsp_queue = rsp_queue
        self.cust_check_interval = interval
        self.cust_list = CustManager.cust_list

    def get_cfg_list(self, cust):
        channle_list = {}
        for channle_name in SmsConfig.channle_list.keys():
            try:
                channle_cfg = getattr(cust, channle_name)
                channle_list[channle_name] = channle_cfg
            except:
                pass
        return channle_list

    @keep_interval
    @keep_db_alive
    def cust_check(self):
        cust_dept_list = Dept.objects.filter(processor__pid=self.pid)
        for cust_dept in self.cust_list.keys():
            if cust_dept not in cust_dept_list:
                self.delete_cust(cust_dept)
        for cust_dept in cust_dept_list:
            if cust_dept in self.cust_list:
                self.update_cust(cust_dept)
            else:
                self.insert_cust(cust_dept)

    def insert_cust(self, cust_dept):
        cfg_list = self.get_cfg_list(cust_dept)
        self.cust_list[cust_dept] = {}

        for channle_name in SmsConfig.channle_list.keys():
            channle_cfg = cfg_list.get(channle_name)
            if channle_cfg and getattr(channle_cfg,
                                       SmsConfig.channle_list.get(channle_name).get('status_field')) == 'enabled':
                self.cust_list[cust_dept][channle_name] = load_cls(
                    SmsConfig.channle_list.get(channle_name).get('client'))(channle_cfg)
                self.cust_list[cust_dept][channle_name].start_serv()
                print '#%d insert %s %s' % (self.pid, cust_dept, channle_name)

    def delete_cust(self, cust_dept):
        client_list = self.cust_list.get(cust_dept)
        for channle_name in SmsConfig.channle_list.keys():
            channle_client = client_list.get(channle_name)
            if channle_client:
                channle_client.stop_serv()
                client_list.pop(channle_name)
                print '#%d delete %s %s' % (self.pid, cust_dept, channle_name)
        self.cust_list.pop(cust_dept)

    def update_cust(self, cust_dept):
        cfg_list = self.get_cfg_list(cust_dept)
        client_list = self.cust_list.get(cust_dept)
        for channle_name in SmsConfig.channle_list.keys():
            channle_cfg = cfg_list.get(channle_name)
            channle_client = client_list.get(channle_name)
            if (channle_cfg and getattr(channle_cfg, SmsConfig.channle_list.get(channle_name).get(
                    'status_field')) == 'enabled') and not channle_client:
                self.cust_list[cust_dept][channle_name] = load_cls(
                    SmsConfig.channle_list.get(channle_name).get('client'))(channle_cfg)
                self.cust_list[cust_dept][channle_name].start_serv()
                print '#%d insert %s %s' % (self.pid, cust_dept, channle_name)
            elif not (channle_cfg and getattr(channle_cfg, SmsConfig.channle_list.get(channle_name).get(
                    'status_field')) == 'enabled') and channle_client:
                channle_client.stop_serv()
                client_list.pop(channle_name)
                print '#%d delete %s %s' % (self.pid, cust_dept, channle_name)
            else:
                pass

    def run(self):
        django_setup()
        import sms.serv.smstools
        task_loader = sms.serv.smstools.CommonSendTaskLoader()
        while True:
            try:
                self.cust_check()
                task_loader.fetch_new_task()

            except:
                log("SMS_MANAGER_ERROR", logger='sms', level='error')
                # traceback.print_exc()
                pass
            sleep(1)


class DaemonProcess:
    def __init__(self, req_queue, rsp_queue, interval=10, main=False):
        self.req_queue = req_queue
        self.rsp_queue = rsp_queue
        self.clear_task_interval = interval
        self.main = main

    def run(self):
        while True:
            try:
                if self.main:
                    self.clear_task()
            except:
                pass
            sleep(1)

    @keep_interval
    @keep_db_alive
    def clear_task(self):
        task_list = SendTaskClear.clear_all_quick()
        if task_list:
            print 'clear task', task_list

    @keep_db_alive
    def set_max_id(self):
        SendTaskClear.set_max_id()
