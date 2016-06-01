# -*- coding: utf-8 -*-
from django.db.models import Q
from django.db.models.query import QuerySet

from X.tools.exception import VerifyException
from base.models import User
from extra.models import SI_Contract, SI_Pay, SI_Invoice, SI_EmptyPay


def model_filter(request, query):
    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')

    model = query.model

    if model == SI_Contract:
        if cur_user.role.type in ['super']:
            pass
        elif cur_user.role.type in ['admin']:
            query = query.filter(user__dept__root_id=dept_root_id)
        else:
            query = query.filter(
                user=cur_user
            )

    elif model == SI_Pay:
        if cur_user.role.type in ['super']:
            pass
        elif cur_user.role.type in ['admin']:
            query = query.filter(user__dept__root_id=dept_root_id)
        else:
            query = query.filter(
                Q(user=cur_user) | Q(user__dept__root_id=dept_root_id, pay_stat='init')
            )

    elif model == SI_Invoice:
        if cur_user.role.type in ['super']:
            pass
        elif cur_user.role.type in ['admin']:
            query = query.filter(pay__user__dept__root_id=dept_root_id)
        else:
            query = query.filter(
                Q(pay__user=cur_user) | Q(pay__user__dept__root_id=dept_root_id, pay__pay_stat='init')
            )

    elif model == SI_EmptyPay:
        if cur_user.role.type in ['super']:
            pass
        else:
            query = query.filter(user__dept__root_id=dept_root_id)

    return query


def model_default(request, obj_list, method='insert'):  # fill->default->check
    if type(obj_list) not in (list, QuerySet) and str(
            type(obj_list)) != "<class 'django.db.models.fields.related.RelatedManager'>":
        obj_list = [obj_list, ]

    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')
    for obj in obj_list:
        if type(obj) == SI_Contract:
            si_contract = obj
            if method == 'insert':
                si_contract.user = cur_user

        elif type(obj) == SI_Pay:
            si_pay = obj
            if method == 'insert':
                si_pay.user = cur_user;

        elif type(obj) == SI_Invoice:
            si_invoice = obj

        elif type(obj) == SI_EmptyPay:
            si_empty_pay = obj


def model_check(request, obj_list):  # for insert,update,delete. before save()
    if type(obj_list) not in (list, QuerySet) and str(
            type(obj_list)) != "<class 'django.db.models.fields.related.RelatedManager'>":
        obj_list = [obj_list, ]

    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')
    for obj in obj_list:
        if type(obj) == SI_Contract:
            si_contract = obj
            if cur_user.role.type in ['super']:
                pass
            elif cur_user.role.type in ['admin']:
                if not si_contract.user.dept.root_id == dept_root_id:
                    raise VerifyException(u"禁止操作非本单位合同！")
            else:
                if not si_contract.user == cur_user:
                    raise VerifyException(u"禁止操作他人合同！")

        elif type(obj) == SI_Pay:
            si_pay = obj
            if cur_user.role.type in ['super']:
                pass
            elif cur_user.role.type in ['admin']:
                if not si_pay.user.dept.root_id == dept_root_id:
                    raise VerifyException(u"禁止操作非本单位报账单！")
            else:
                if not (si_pay.user == cur_user
                        or si_pay.user.dept.root_id == dept_root_id and si_pay.pay_stat == 'init'):
                    raise VerifyException(u"禁止操作他人报账单！")

        elif type(obj) == SI_Invoice:
            si_invoice = obj
            if cur_user.role.type in ['super']:
                pass
            elif cur_user.role.type in ['admin']:
                if not si_invoice.pay.user.dept.root_id == dept_root_id:
                    raise VerifyException(u"禁止操作非本单位发票！")
            else:
                if not (si_invoice.pay.user == cur_user
                        or si_invoice.pay.user.dept.root_id == dept_root_id and si_invoice.pay.pay_stat == 'init'):
                    raise VerifyException(u"禁止操作他人发票")

            if not si_invoice.pay.pay_stat == 'allot':
                raise VerifyException(u"禁止在报账单状态为非已分配时操作发票！")

        elif type(obj) == SI_EmptyPay:
            si_empty_pay = obj
