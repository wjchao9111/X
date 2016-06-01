#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

import django

import X.settings
from X.tools import load_cls

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


def gen_model_js(cls_path):
    cls_name = cls_path.split('.')[-1]
    cls = load_cls(cls_path)
    model_js_name = cls_name + 'Model.js'
    model_js_content = "Ext.define('X.model.%sModel', {extend: 'Ext.data.Model',fields: [" % cls_name
    for field in cls._meta.fields:
        if field.name == 'id':
            model_js_content += "\r\n{name: '%s', label: '%s', show: true, field: 'hiddenfield'}," % (
                field.name, u"编号")

        elif field.choices:
            model_js_content += "\r\n{name: '%s', label: '%s', field: 'combo', choice: '####.####'%s}," % (
                field.name, field.verbose_name, field.blank and ',blank:true' or '')
            model_js_content += "\r\n{name: '%s_display', label: '%s', show: true%s}," % (
                field.name, field.verbose_name, field.blank and ',blank:true' or '')

        elif type(field).__name__ == 'ForeignKey':
            model_js_content += "\r\n{name: '%s_id', label: '%s', field: 'combo', store: 'X.store.%sStore'%s}," % (
                field.name, field.verbose_name, field.related_model.__name__, field.blank and ',blank:true' or '')
            model_js_content += "\r\n{name: '%s', label: '%s', show: true%s}," % (
                field.name, field.verbose_name, field.blank and ',blank:true' or '')

        elif type(field).__name__ == 'FileField':
            model_js_content += "\r\n{name: '%s', label: '%s', field: 'filefield'%s}," % (
                field.name, field.verbose_name, field.blank and ',blank:true' or '')

        elif type(field).__name__ == 'DateField':
            model_js_content += "\r\n{name: '%s', label: '%s', show: true, field: 'datefield',field_cfg: {format: 'Y-m-d'}%s}," % (
                field.name, field.verbose_name, field.blank and ',blank:true' or '')

        elif type(field).__name__ == 'DateTimeField':
            model_js_content += "\r\n{name: '%s', label: '%s', show: true%s}," % (
                field.name, field.verbose_name, field.blank and ',blank:true' or '')

        else:
            model_js_content += "\r\n{name: '%s', label: '%s', show: true, field: 'textfield'%s}," % (
                field.name, field.verbose_name, field.blank and ',blank:true' or '')

    model_js_content = model_js_content[:-1]
    model_js_content += " ]});"
    print "=" * 10, model_js_name, "=" * 10
    print model_js_content


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for cls_path in sys.argv[1:]:
            gen_model_js(cls_path)
