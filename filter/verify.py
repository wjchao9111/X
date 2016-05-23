# -*- coding: utf-8 -*-
import re

from django.db.models.query import QuerySet

from X.tools.exception import VerifyException
from base.models import User
from filter.models import Cmpp2Cfg, WhiteList, Filter


def get_filter_cmpp2cfg_by_user(user):
    try:
        return user.dept.root.filter_cmpp2cfg
    except:
        return None


def get_regex(text):
    for ch in r'\^$.*+-?=!:|/()[]{}':
        text = text.replace(ch, '\\' + ch)
    regex, count = re.subn(r'(\\\[\\\[.+?\\\]\\\])', '.+', text)
    return '^%s$' % regex


def model_filter(request, query):
    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')

    model = query.model

    if model == Cmpp2Cfg:
        query = query

    elif model == WhiteList:
        query = query

    elif model == Filter:
        if cur_user.role.type in ['super']:
            query = query
        else:
            query = query.filter(user__dept__root_id=dept_root_id)

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

        elif type(obj) == WhiteList:
            whitelist = obj

        elif type(obj) == Filter:
            filter = obj
            if cur_user.role.type in ['super']:
                if method == 'insert':
                    raise VerifyException()
            else:
                filter.stat = 'new'
                filter.user = cur_user

                cmpp_cfg = get_filter_cmpp2cfg_by_user(cur_user)
                if cmpp_cfg == None:
                    raise VerifyException()
                filter.cmpp_cfg = cmpp_cfg

            filter.regex = get_regex(filter.text)


def model_check(request, obj_list):
    if type(obj_list) not in (list, QuerySet) and str(
            type(obj_list)) != "<class 'django.db.models.fields.related.RelatedManager'>":
        obj_list = [obj_list, ]

    # super：type must be admin, dept.root = this.root
    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')
    for obj in obj_list:
        if type(obj) == Cmpp2Cfg:
            cmpp2 = obj

        elif type(obj) == WhiteList:
            whitelist = obj

        if type(obj) == Filter:
            filter = obj
            if cur_user.role.type in ['super']:
                pass
            else:
                if filter.user.dept.root_id != dept_root_id:
                    raise VerifyException()
