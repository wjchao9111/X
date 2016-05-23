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

from X.tools.task import sleep

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from filter.serv.forward import FORWARD_SERVER

cfg_list = []
if not cfg_list:
    cfg_list.append({'serv_addr': ('0.0.0.0', 8000), 'forward_addr': ('111.11.84.251', 80)})
for cfg in cfg_list:
    serv_addr = cfg.get('serv_addr')
    forward_addr = cfg.get('forward_addr')
    server = FORWARD_SERVER(serv_addr=serv_addr, forward_addr=forward_addr)

while True:
    sleep(1)
