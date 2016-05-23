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


from sms.serv.smsfile import FileManager
from X.tools.task import sleep
file_manager = FileManager()

while True:
    sleep(1)
    file_manager.fetch_new_task()