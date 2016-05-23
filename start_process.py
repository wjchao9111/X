#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
    import pwd
    import os

    os.setgid(pwd.getpwnam('apache').pw_gid)
    os.setuid(pwd.getpwnam('apache').pw_uid)
except:
    pass

import sys
import os
from multiprocessing import freeze_support, Manager, Pool

import X.settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

X.settings.DEBUG = False
os.environ['DJANGO_SETTINGS_MODULE'] = 'X.settings'


def start_channle_process(pid, req_queue, rsp_queue, interval):
    from sms.serv.smsmanager import ChannleProcess
    p = ChannleProcess(pid, req_queue, rsp_queue, interval)
    p.run()


def start_daemon_process(req_queue, rsp_queue, interval, main=False):
    django_setup()
    from sms.serv.smsmanager import DaemonProcess
    p = DaemonProcess(req_queue, rsp_queue, interval, main)
    p.run()


# from sms.serv.cmpp2manager import *

def django_setup():
    import django
    v1, v2 = django.VERSION[:2]
    if v1 == 1 and v2 > 4:
        django.setup()
    if v1 == 1 and v2 <= 4:
        import django.core.management
        getattr(django.core.management, 'setup_environ')(X.settings)


if __name__ == '__main__':
    freeze_support()
    interval = 10
    pid_list = [0, ]
    size = len(pid_list)

    # pool mode

    pool = Pool(processes=size)
    manager = Manager()
    req_queue = manager.Queue()
    rsp_queue = manager.Queue()
    for pid in pid_list:
        pool.apply_async(start_channle_process, (pid, req_queue, rsp_queue, interval))

    start_daemon_process(req_queue, rsp_queue, interval, main=0 in pid_list)
