#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import json

import django

import X.settings
from X.tools.middleware import http_403_error

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

from X.views import choices

choices_str = json.dumps(choices)

open('X/static/ExtJS/x-all.js', 'w').write("var kv_data='%s';\n" % choices_str)
open('X/static/ExtJS/x-all.js', 'a').write("var http_403_error='%s';\n" % http_403_error)
os.system('cat X/static/ExtJS/util/*.js >> X/static/ExtJS/x-all.js')
os.system('cat X/static/ExtJS/model/*.js >> X/static/ExtJS/x-all.js')
os.system('cat X/static/ExtJS/store/*.js >> X/static/ExtJS/x-all.js')
os.system('cat X/static/ExtJS/view/*.js >> X/static/ExtJS/x-all.js')
