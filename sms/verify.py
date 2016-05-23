# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet

from X.tools.exception import VerifyException
from base.models import User
from sms.models import Cmpp2Cfg, QtppCfg, CarrierSection, SendTask, MsgSend, MsgRecv


def model_filter(request, query):
    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')

    model = query.model

    if model == Cmpp2Cfg:
        query = query

    elif model == QtppCfg:
        query = query

    elif model == CarrierSection:
        query = query

    elif model == SendTask or model.__name__.startswith('SendTask'):
        if cur_user.role.type in ['super']:
            pass
        elif cur_user.role.type in ['admin']:
            query = query.filter(user__dept__root_id=dept_root_id)
        else:
            query = query.filter(
                user=cur_user
            )

    elif model == MsgSend or model.__name__.startswith('MsgSend'):
        if cur_user.role.type in ['super']:
            pass
        elif cur_user.role.type in ['admin']:
            query = query.filter(msg_user__dept__root_id=dept_root_id)
        else:
            query = query.filter(
                msg_user=cur_user
            )

    elif model == MsgRecv:
        query = query.filter(
            msg_user=cur_user
        )

    return query


def model_default(request, obj_list, method='insert'):
    if type(obj_list) not in (list, QuerySet) and str(
            type(obj_list)) != "<class 'django.db.models.fields.related.RelatedManager'>":
        obj_list = [obj_list, ]

    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')
    for obj in obj_list:
        if type(obj) == Cmpp2Cfg:
            cmpp2 = obj

        elif type(obj) == QtppCfg:
            qtpp = obj

        elif type(obj) == CarrierSection:
            section = obj

        elif type(obj) == SendTask:
            task = obj
            if method == 'insert':
                task.user = cur_user
                task.priority = imax(task.priority, cur_user.priority)
                task.suffix = cur_user.suffix


def imax(a, b):
    try:
        a = int(a)
    except:
        a = 99
    try:
        b = int(b)
    except:
        b = 99
    return max(a, b)


def model_check(request, obj_list):
    if type(obj_list) not in (list, QuerySet) and str(
            type(obj_list)) != "<class 'django.db.models.fields.related.RelatedManager'>":
        obj_list = [obj_list, ]

    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')
    for obj in obj_list:
        if type(obj) == Cmpp2Cfg:
            cmpp2 = obj

        elif type(obj) == QtppCfg:
            qtpp = obj

        elif type(obj) == CarrierSection:
            section = obj

        elif type(obj) == SendTask:
            task = obj

            if not (task.user == cur_user):
                raise VerifyException()
