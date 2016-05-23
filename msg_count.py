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

from sms.models import *
from sms.views import get_msg_count

modle_list = [
    MsgSend,
    MsgSend01,
    MsgSend02,
    MsgSend03,
    MsgSend04,
    MsgSend05,
    MsgSend06,
    MsgSend07,
    MsgSend08,
    MsgSend09,
    MsgSend10,
    MsgSend11,
    MsgSend12,
]

for model in modle_list:
    print model
    for msg in model.objects.filter(msg_count=0):
        msg.msg_count = get_msg_count(msg)
        msg.save()
