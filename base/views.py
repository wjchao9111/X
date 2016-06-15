# -*- coding: utf-8 -*-

import time

from X.tools import get_random_num
from X.tools.mail import send_mail
from X.tools.middleware import JsonResponse
from X.tools.model import get_object
from base.models import User, Role, Permission
from base.verify import model_check, model_filter
from sms.tasks import send_task_prepare_sync
from sms.views import get_task


# Create your views here.

def user_has_cmpp2cfg(user):
    try:
        if user.dept.root.cmpp2cfg:
            return True
        else:
            return False
    except:
        return False


def user_verify(request, method):
    obj = request.json['object']

    query = User.objects.filter(code=obj['code'])
    success = False
    user = None
    if query.count() == 1:
        user = query[0]
        if user.pwd == obj['pwd']:
            if user.stat == 'normal':
                success = True
            else:
                message = "账户被锁定！"
        else:
            message = "密码错误！"
    else:
        message = "账号不存在！"

    verify_code = get_random_num(6)
    request.session['verify_code'] = verify_code
    request.session['verify_expire'] = time.time() + 60 * 5

    if success:
        if method == 'sms' and user_has_cmpp2cfg(user):
            j_task = {
                'type': 'default',
                'name': '系统验证码',
                'priority': 1,
                'content': verify_code,
                'phones': user.phone,
                'suffix': user.suffix,
            }
            task = get_task(j_task)
            task.user_id = user.id
            task.save()
            send_task_prepare_sync(task)
            message = '获取短信验证码成功！'
        else:  # elif method == 'email':
            send_mail([user.email], u'系统验证码', verify_code)
            message = '获取Email验证码成功！'
    return JsonResponse({'success': success, 'message': message})


def user_login(request):
    obj = request.json['object']

    query = User.objects.filter(code=obj['code'])
    success = False
    message = ""
    if query.count() == 1:
        user = query[0]
        if user.pwd == obj['pwd']:
            if user.stat == 'normal':
                if request.session.get('verify_expire', 0) > time.time():
                    if request.session.get('verify_code') == obj.get('verify'):
                        request.session.pop('verify_expire')
                        request.session.pop('verify_code')
                        dept_root = user.dept.root and user.dept.root or user.dept
                        admin = get_object(dept_root.dept_user_set, role__type='admin', admin=dept_root)
                        request.session['user'] = {
                            'id': user.id,
                            'name': user.name,
                            'code': user.code,
                            'type': user.role.type,
                            'dept_id': user.dept.id,
                            'dept_name': user.dept.name,
                            'dept_path': user.dept.path,
                            'dept_root_id': dept_root.id,
                            'dept_root_name': dept_root.name,
                            'admin_id': admin is not None and admin.id or None,
                        }
                        success = True
                    else:
                        message = '验证码错误！'
                else:
                    message = "验证码过期！"
            else:
                message = "账户被锁定！"
        else:
            message = "密码错误！"
    else:
        message = "账号不存在！"

    return JsonResponse({'success': success, 'message': message})


def user_logout(request):
    if 'user' in request.session:
        request.session.pop('user')
        request.session.pop('urls')
    success = True
    message = '注销成功！'
    return JsonResponse({'success': success, 'message': message})


def user_info(request):
    user = request.session.get('user')
    return JsonResponse({'user': user})


def get_perm_tree(perm_list, visited=None, root=None):
    if not visited:
        visited = []
    node_list = []
    for perm in perm_list:
        if perm.parent == root and perm not in visited:
            node = {
                'id': perm.id,
                'text': perm.name,
                'url': perm.value,
                'cls': None,
                'qtip': perm.note,
            }
            visited.append(perm)
            node_list.append(node)
            children = get_perm_tree(perm_list, visited=visited, root=perm)
            if children:
                node['leaf'] = False
                node['children'] = children
            else:
                node['leaf'] = True
    return node_list


def menu_or_ajax(perm_list):
    menu_list = []
    ajax_list = []
    for perm in perm_list:
        if perm.type == 'menu':
            menu_list.append(perm)
        elif perm.type == 'ajax':
            ajax_list.append(perm)
    return menu_list, ajax_list


def user_perm(request):
    user = request.session.get('user')
    user = User.objects.get(pk=user.get('id'))

    perm_list = Permission.objects.all()
    perm_list = model_filter(request, perm_list)

    menu_list, ajax_list = menu_or_ajax(perm_list)
    request.session['urls'] = [ajax.value for ajax in ajax_list]

    perm_tree = get_perm_tree(menu_list, visited=[], root=None)
    return JsonResponse(perm_tree)


def user_reset_pass(request):
    obj = request.json['object']
    user = get_object(User, code=obj.get('code'))
    if user.pwd == obj.get('old_pwd'):
        user.pwd = obj.get('pwd')
        user.save()
        return JsonResponse({'success': True, 'message': '成功！'})
    else:
        return JsonResponse({'success': False, 'message': '原密码错误！'})


def get_perm_tree_checked(perm_list, checked_list, visited=None, root=None):
    if not visited:
        visited = []
    node_list = []
    for perm in perm_list:
        if perm.parent == root and perm not in visited:
            node = {
                'id': perm.id,
                'text': perm.name,
                'url': perm.value,
                'cls': None,
                'qtip': perm.note,
                'checked': perm in checked_list,
            }
            visited.append(perm)
            node_list.append(node)
            children = get_perm_tree_checked(perm_list, checked_list, visited=visited, root=perm)
            if children:
                node['leaf'] = False
                node['children'] = children
            else:
                node['leaf'] = True
    return node_list


def role_perm(request):
    obj = request.json['role']
    role = get_object(Role, pk=obj.get('id'))
    role_perm_list = role.perm.all()
    perm_list = Permission.objects.all()

    model_check(request, role)
    perm_list = model_filter(request, perm_list)

    perm_tree = get_perm_tree_checked(perm_list, role_perm_list, [], None)
    return JsonResponse(perm_tree)


def role_perm_update(request):
    obj = request.json['role']
    ids = request.json['ids']
    role = get_object(Role, pk=obj.get('id'))
    if ids:
        id_list = ids.split(',')
    else:
        id_list = []
    perm_list = Permission.objects.all().filter(id__in=[id for id in id_list])

    model_check(request, role)
    perm_list = model_filter(request, perm_list)

    role.perm = perm_list
    return JsonResponse({'success': True, 'message': '成功！'})
