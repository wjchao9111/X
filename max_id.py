#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os

import django

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

from sms.serv.smstools import SendTaskClear

SendTaskClear.set_max_id()
