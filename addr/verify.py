# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet
from django.db.models import Q

from X.tools.exception import VerifyException
from base.models import User
from addr.models import Address, AddressGroup, AddressFile


def model_filter(request, query):
    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')

    model = query.model

    if model == AddressGroup:
        query = query.filter(
            Q(
                Q(user=cur_user) |
                Q(dept_id=dept_id, mod__in=get_mod_list(1, 'group')) |
                Q(mod__in=get_mod_list(1, 'all'))
            ) & Q(dept__root_id=dept_root_id)
        )

    elif model == Address:
        query = query.filter(
            Q(
                Q(group__user=cur_user) |
                Q(group__dept=cur_user.dept, group__mod__in=get_mod_list(1, 'group')) |
                Q(group__mod__in=get_mod_list(1, 'all'))
            ) & Q(group__dept__root_id=dept_root_id)
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
        if type(obj) == AddressGroup:
            grp = obj
            if method == 'insert':
                grp.dept_id = dept_id
                grp.user = cur_user

        elif type(obj) == Address:
            addr = obj

        elif type(obj) == AddressFile:
            file = obj
            if method == 'insert':
                file.user = cur_user


def model_check(request, obj_list):
    if type(obj_list) not in (list, QuerySet) and str(
            type(obj_list)) != "<class 'django.db.models.fields.related.RelatedManager'>":
        obj_list = [obj_list, ]

    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')
    for obj in obj_list:
        if type(obj) == AddressGroup:
            grp = obj
            if not (
                            (grp.user == cur_user) or
                            (grp.dept_id == dept_id and grp.mod in get_mod_list(3, 'group')) or
                            grp.mod in get_mod_list(3, 'all')
            ): raise VerifyException()

        elif type(obj) == Address:
            addr = obj
            grp = addr.group

            if not (
                            (grp.user == cur_user) or
                            (grp.dept_id == dept_id and grp.mod in get_mod_list(2, 'group')) or
                            grp.mod in get_mod_list(2, 'all')
            ):
                raise VerifyException()
        elif type(obj) == AddressFile:
            file = obj
            grp = file.group

            if not (
                            (grp.user == cur_user) or
                            (grp.dept_id == dept_id and grp.mod in get_mod_list(2, 'group')) or
                            grp.mod in get_mod_list(2, 'all')
            ):
                raise VerifyException()


def get_mod_list(level, user):
    m_all = ['0', '1', '2', '3']
    m_level = {0: ['0', '1', '2', '3'], 1: ['1', '2', '3'], 2: ['2', '3'], 3: ['3']}[level]
    m_result = []
    if user == 'group':
        for i in m_all:
            for j in m_level:
                m_result.append(i + j)
    elif user == 'all':
        for i in m_all:
            for j in m_level:
                m_result.append(j + i)

    return m_result
