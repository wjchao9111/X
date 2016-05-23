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

import django

from X.tools.task import sleep
import X.settings

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


from filter.serv.cmpp2filter import CMPP2_SERVER

cfg_list = []
if not cfg_list:
    cfg_list.append({'ip': '0.0.0.0', 'port': 7890, 'ssl_mode': 0})
    cfg_list.append({'ip': '0.0.0.0', 'port': 17890, 'ssl_mode': 1})
for cfg in cfg_list:
    ip = cfg['ip']
    port = cfg['port']
    ssl_mode = cfg['ssl_mode']
    server = CMPP2_SERVER(serv_addr=(ip, port), ssl_mode=ssl_mode)
    # print "CMPP2_SERVER RUN AT %s"%(str(server.serv_addr))

# raw_input("click any key to continue\n")

while True:
    sleep(1)
