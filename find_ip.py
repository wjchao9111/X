#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os

import django

import X.settings
from X.tools.task import gevent_task, sleep, socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

X.settings.DEBUG = False

os.environ['DJANGO_SETTINGS_MODULE'] = 'X.settings'
v1, v2 = django.VERSION[:2]
if v1 == 1 and v2 > 4:
    django.setup()
if v1 == 1 and v2 <= 4:
    import django.core.management

    getattr(django.core.management, 'setup_environ')(X.settings)

from sms.serv.socketlib import SocketClient
from sms.models import Cmpp2Cfg
from filter.models import Cmpp2Cfg as FilterCfg

base_ip = '111.11.84'
all_ip = [[41, 139], [141, 250], ]

ip_list = []
for ip_cfg in all_ip:
    ip_list += range(ip_cfg[0], ip_cfg[1] + 1)
ip_list = ['%s.%s' % (base_ip, ip) for ip in ip_list]


@gevent_task
def test_ip(ip):
    try:
        sock = SocketClient((ip, 0), ('218.207.67.136', '7890'))
        sock.connect()
        print 'USED', ip
    except:
        print 'UNUSED', ip


managed_ip = [
                 cfg.sock_source_ip for cfg in Cmpp2Cfg.objects.all()
                 ] + [
                 cfg.sock_source_ip for cfg in FilterCfg.objects.all()
                 ]

socket.setdefaulttimeout(3)

print 'MANAGED IP:'
for ip in ip_list:
    if ip in managed_ip:
        test_ip(ip)

for i in range(5):
    sleep(1)

print 'UNMANAGED IP:'
for ip in ip_list:
    if ip not in managed_ip:
        test_ip(ip)
for i in range(5):
    sleep(1)
