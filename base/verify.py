# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet
from django.db.models import F, Q

from X.tools.exception import VerifyException
from base.models import User, Role, Permission, Dept

user_role_tag = '-PUB'


def model_filter(request, query):
    cur_user = User.objects.get(pk=request.session.get('user').get('id'))
    dept_path = request.session.get('user').get('dept_path')
    dept_id = request.session.get('user').get('dept_id')
    dept_root_id = request.session.get('user').get('dept_root_id')

    model = query.model

    if model == Dept:
        if cur_user.role.type in ['super']:
            query = query.filter(
                type='company',
                stat='normal',
                root_id=F('id')
            )
        else:
            query = query.filter(
                type__in=['company', 'dept'],
                stat='normal',
                root_id=dept_root_id,
                path__startswith=dept_path
            )

    elif model == Role:
        if cur_user.role.type in ['super']:
            query = query.filter(
                type__in=['admin', 'user'],
                stat='normal',
                dept_id=dept_id
            )
        else:
            query = query.filter(
                Q(type='user', stat='normal') & (
                    Q(dept__root_id=dept_root_id) |
                    Q(dept__type='system', dept__name='system')
                )
            )

    elif model == User:
        if cur_user.role.type in ['super']:
            query = query.filter(
                # stat = 'normal',
                role__type='admin',
                role__dept_id=dept_id,
                dept__type='company',
                dept__root_id=F('dept_id')
            )
        else:
            query = query.filter(
                stat='normal',
                role__type='user',
                # role__dept__root_id=dept_root_id,
                # role__dept__path__startswith=dept_path,
                dept__type__in=['dept', 'company'],
                dept__root_id=dept_root_id,
                dept__path__startswith=dept_path
            )
    elif model == Permission:
        if cur_user.role.type in ['super']:
            query = query
        else:
            admin = User.objects.get(pk=request.session.get('user').get('admin_id'))
            query = query.filter(id__in=list(set([perm.id for perm in admin.role.perm.all()]) & set(
                [perm.id for perm in cur_user.role.perm.all()])))
        query = query.filter(stat='normal')
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
        if type(obj) == Dept:
            dept = obj
            dept.save()
            if cur_user.role.type in ['super']:
                if dept.parent_id == dept.id:
                    dept.parent_id = None

                if method == 'insert':
                    dept.type = 'company'
                    dept.root = dept
            # admin or user: type must be user, role.dept.root = dept.root = this.root
            else:
                if dept.parent_id == dept.id:
                    dept.parent_id = dept.id

                if method == 'insert':
                    dept.type = 'dept'
                    dept.root_id = dept_root_id
                if not dept.parent_id and dept.id != dept_id:
                    dept.parent_id = dept_id

            dept.set_path()

        elif type(obj) == Role:
            role = obj
            if cur_user.role.type in ['super']:
                if role.name.endswith(user_role_tag):
                    role.type = 'user'
                else:
                    role.type = 'admin'

                if method == 'insert':
                    role.dept = cur_user.dept
            else:
                if method == 'insert':
                    role.type = 'user'
                    role.dept = cur_user.dept

        elif type(obj) == User:
            user = obj
            if cur_user.role.type in ['super']:
                user.admin = user.dept
            else:
                pass
        elif type(obj) == Permission:
            perm = obj

            if perm.parent_id == perm.id:
                perm.parent_id = None

            if cur_user.role.type in ['super']:
                pass
            else:
                pass


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
        if type(obj) == Dept:
            dept = obj
            if cur_user.role.type in ['super']:
                if False \
                        or not dept.type == 'company' \
                        or not dept.root_id == dept.id:
                    raise VerifyException()
            # admin or user: type must be user, role.dept.root = dept.root = this.root
            else:
                if False \
                        or not dept.type == 'dept' \
                        or not dept.path.startswith(dept_path) \
                        or not dept.root_id == dept_root_id \
                        or not (dept.parent and dept.parent.root_id == dept_root_id) \
                        or not (dept.parent and dept.parent.path.startswith(dept_path)):
                    raise VerifyException()

        elif type(obj) == Role:
            role = obj
            if cur_user.role.type in ['super']:
                # or not role.type == 'admin' \
                if False \
                        or not role.dept_id == dept_id:
                    raise VerifyException()
            # admin or user: type must be user, role.dept.root = dept.root = this.root
            else:
                if False \
                        or not role.type == 'user' \
                        or not role.dept.root_id == dept_root_id \
                        or not role.dept.path.startswith(dept_path):
                    raise VerifyException()

        elif type(obj) == User:
            user = obj
            if cur_user.role.type in ['super']:
                if False \
                        or not user.role.type == 'admin' \
                        or not user.role.dept_id == dept_id \
                        or not user.dept.type == 'company' \
                        or not user.dept.root_id == user.dept.id:
                    raise VerifyException()
            # admin or user: type must be user, role.dept.root = dept.root = this.root
            # or not (user.role.dept.root_id == dept_root_id) \
            else:
                if False \
                        or not user.role.type == 'user' \
                        or user.dept.type not in ['dept', 'company'] \
                        or not dept_path.startswith(user.role.dept.path) \
                        or not user.dept.root_id == dept_root_id \
                        or not user.dept.path.startswith(dept_path):
                    raise VerifyException()
        elif type(obj) == Permission:
            perm = obj
            if cur_user.role.type in ['super']:
                pass
            else:
                raise VerifyException()
