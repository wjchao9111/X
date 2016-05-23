# -*- coding: utf-8 -*-
import os
import uuid

from django.db import connection, connections
from django.db.models import Model, Q
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.http import FileResponse
from xlwt import Workbook

from X import settings
from X.settings import TEMP_ROOT
from X.tools import load_cls
from X.tools.middleware import JsonResponse
from sms.models import SendTask, MsgSend, Cmpp2Send, QtppSend


def get_object(Model, *args, **kwargs):
    try:
        if type(Model) == QuerySet or str(type(Model)) == "<class 'django.db.models.fields.related.RelatedManager'>":
            return Manager.get(Model, *args, **kwargs)
        return Manager.get(Model.objects, *args, **kwargs)
    except:
        return None


def keep_db_alive(function):
    def decorator(*args, **kwargs):
        try:
            connection.connection.ping()
        except:
            connection.close()
        try:
            connections['slave'].connection.ping()
        except:
            connections['slave'].close()
        return function(*args, **kwargs)

    return decorator


def keep_slave_db_alive(function):
    def decorator(*args, **kwargs):
        try:
            connections['slave'].connection.ping()
        except:
            connections['slave'].close()
        return function(*args, **kwargs)

    return decorator


class DBRouter(object):
    def db_for_read(self, model, **hints):
        if model in [SendTask, MsgSend, Cmpp2Send, QtppSend]:
            return 'default'
        return 'slave'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        return True


def export_excel(model, obj_list):
    file_name = str(uuid.uuid1())
    file_path = os.path.join(TEMP_ROOT, file_name)
    wb = Workbook(encoding='utf-8')
    ws = wb.add_sheet('Export')
    if model and obj_list:
        meta_fields = model._meta.fields
        cols = 0
        for field in meta_fields:
            fs = [field.name + '_id', field.name, field.name + '_display']
            for f in fs:
                if f in obj_list[0]:
                    ws.write(0, cols, field.verbose_name)
                    cols += 1
        rows = 1
        for obj in obj_list:
            cols = 0
            for field in meta_fields:
                fs = [field.name + '_id', field.name, field.name + '_display']
                for f in fs:
                    if f in obj:
                        try:
                            value = unicode(obj.get(f))
                        except:
                            value = obj.get(f)
                        ws.write(rows, cols, value)
                        cols += 1
            rows += 1
    else:
        ws.write(0, 0, u'导出数据为空！')
    wb.save(file_path)
    response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % 'Export.xls'
    return response


def object_list(function):
    def decorator(*args, **kwargs):
        request, args = args[0], args[1:]
        json = request.json

        export = kwargs.get('export')
        if 'export' in kwargs:
            kwargs.pop('export')

        if export == None:
            page = int(json['page'])
            start = int(json['start'])
            limit = int(json['limit'])

        query = json.get('query')

        query_field = kwargs.get('query_field', [])
        if 'query_field' in kwargs:
            kwargs.pop('query_field')

        hide_field = kwargs.get('hide_field', [])
        if 'hide_field' in kwargs:
            kwargs.pop('hide_field')

        qs = function(request, *args, **kwargs)

        if query:
            q = Q(**{'id' + '__contains': query})
            for field in query_field:
                q = q | Q(**{field + '__contains': query})
            qs = qs.filter(q)

        if export == None:
            obj_count = qs.count()
            model_list = qs[start:limit + start]
        else:
            model_list = qs
        obj_list = []
        model = None
        for model in model_list:
            obj = model.__dict__
            for key in obj.keys():
                if hasattr(model, 'get_%s_display' % key):
                    obj[key + '_display'] = getattr(model, 'get_%s_display' % key)()
                if key.endswith('_id'):
                    key = key[:-3]
                    if hasattr(model, key):
                        val = getattr(model, key)
                        if isinstance(val, Model):
                            obj[key] = str(val)
            for key in obj.keys():
                if key.startswith('_') or key in hide_field:
                    obj.pop(key)
            obj_list.append(obj)

        if export == None:
            return JsonResponse({'object_list': obj_list, 'object_count': obj_count})
        else:
            return export_excel(model, obj_list)

    return decorator


def object_fill(function):
    def decorator(*args, **kwargs):
        request, args = args[0], args[1:]
        obj = request.json.get('object')

        hide_field = kwargs.get('hide_field', [])
        if 'hide_field' in kwargs:
            kwargs.pop('hide_field')

        persist_field = kwargs.get('persist_field', [])
        if 'persist_field' in kwargs:
            kwargs.pop('persist_field')
        persist_field.append('id')

        model = function(request, *args, **kwargs)

        for key in hide_field:
            obj.pop(key)

        meta_fields = [field.name for field in model._meta.fields]
        for key in obj:
            if hasattr(model, key):
                value = obj.get(key)
                if key in persist_field and not obj.get(key):
                    continue
                if (key.endswith('_id') and key[:-3] in meta_fields) or key == 'id':
                    if value == "":
                        value = None
                    else:
                        value = int(value)
                setattr(model, key, value)

        return model

    return decorator


def object_save(function):
    def decorator(*args, **kwargs):
        request, args = args[0], args[1:]
        model = function(request, *args, **kwargs)
        model.save()

    return decorator


def object_delete(function):
    def decorator(*args, **kwargs):
        request, args = args[0], args[1:]
        qs = function(request, *args, **kwargs)
        qs.delete()

    return decorator


def json_success(function):
    def decorator(*args, **kwargs):
        request, args = args[0], args[1:]
        function(request, *args, **kwargs)

        return JsonResponse({'success': True, 'message': '操作成功！'})

    return decorator


app_list = settings.INSTALLED_APPS
filter_list = []
for app in app_list:
    try:
        filter = load_cls(app + '.verify.model_filter')
        filter_list.append(filter)
    except:
        pass


def auto_filter(function):
    def decorator(*args, **kwargs):
        request, args = args[0], args[1:]
        qs = function(request, *args, **kwargs)
        for filter in filter_list:
            qs = filter(request, qs)
        return qs

    return decorator


default_list = []
for app in app_list:
    try:
        default = load_cls(app + '.verify.model_default')
        default_list.append(default)
    except:
        pass


def auto_default(function):
    def decorator(*args, **kwargs):
        request, args = args[0], args[1:]
        obj = function(request, *args, **kwargs)
        for default in default_list:
            if obj.id:
                default(request, obj, 'update')
            else:
                default(request, obj, 'insert')
        return obj

    return decorator


check_list = []
for app in app_list:
    try:
        check = load_cls(app + '.verify.model_check')
        check_list.append(check)
    except:
        pass


def auto_check(function):
    def decorator(*args, **kwargs):
        request, args = args[0], args[1:]
        obj = function(request, *args, **kwargs)
        for check in check_list:
            check(request, obj)
        return obj

    return decorator


@object_list
@auto_filter
def common_list(request, model_type):
    model = load_cls(model_type)
    return model.objects.all()


@json_success
@object_save
@auto_check
@auto_default
@object_fill
def common_save(request, model_type):
    id = request.json.get('object').get('id')
    if id:
        model = load_cls(model_type).objects.get(id=id)
    else:
        model = load_cls(model_type)()
    return model


@json_success
@object_delete
@auto_check
def common_delete(request, model_type):
    ids = request.json.get('ids')
    id_list = ids.split(',')
    qs = load_cls(model_type).objects.filter(id__in=id_list)
    return qs
