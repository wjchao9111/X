#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json

from django.db import IntegrityError
from django.http import HttpResponse
from django.http.request import split_domain_port

from X.tools.exception import VerifyException


# from django.shortcuts import render

class JsonMiddleware:
    def __init__(self):
        pass

    def process_request(self, request):
        request.DATA = {}
        if request.method == "POST":
            request.DATA = request.POST
        if request.method == "GET":
            request.DATA = request.GET
        j_data = {}
        try:
            if request.body and request.body[0] in ['[', '{']:
                j_data = json.loads(request.body)
        except:
            pass
        if j_data:
            request.json = j_data
            return

        j_data = {}
        for key in request.DATA.keys():
            arr = key.split('.')
            tmp = j_data
            for k in arr[:-1]:
                if k not in tmp:
                    tmp[k] = {}
                tmp = tmp[k]
            j = None

            tmp[arr[-1]] = request.DATA[key]
        request.json = j_data

    def process_response(self, request, response):
        if type(response) == JsonResponse:
            return HttpResponse(json.dumps(response.json, cls=JsonEncoder),
                                content_type='text/html')  # content_type="application/json") ie support
        return response


verify_error = 'VerifyError：操作被禁止！<br>可能的原因：<br>1、您正在尝试执行没有权限的读取修改或删除操作，<br>如修改或删除他人建立的通讯录；<br>建议的操作：<br>1、更换有权限的用户重新登陆；<br>2、联系对象的创建者核实操作权限；'
integrity_error = 'IntegrityError：操作已被取消！<br>可能的原因：<br>1、您正在尝试插入重复的值，如添加账号重复的用户；<br>2、关联的对象不存在，如在表单中选择的对象已被删除；<br>建议的操作：<br>1、修改重复的字段；<br>2、刷新浏览器或重新登陆；'
http_403_error = '403 Forbidden：操作被禁止！<br>可能的原因：<br>1、网络状况不佳；<br>2、您未登陆系统；<br>3、登陆会话已超时；<br>4、您正在尝试执行没有权限的操作；<br>建议的操作：<br>1、重新之前的操作；<br>2、刷新浏览器或重新登陆；<br>3、联系您的企业管理员核实操作权限；<br>你知道吗？<br>会话超时被中断怎么办，点击右上角注销链接；<br>重新登陆后可以恢复到注销前的状态；'


class ExceptionMiddleware:
    def __init__(self):
        pass

    def process_exception(self, request, exception):
        if type(exception) == VerifyException:
            return JsonResponse({'success': False, 'message': verify_error})
        if type(exception) == IntegrityError:
            return JsonResponse({'success': False, 'message': integrity_error})


class AuthMiddleware:
    def __init__(self):
        pass

    def process_request(self, request):
        path = request.path
        if (path == '/' or
                path.startswith('/login') or
                path.startswith('/static') or
                path.startswith('/base/user-login') or
                path.startswith('/base/user-verify') or
                path.startswith('/api')):
            return None
        user = request.session.get('user')
        if user:
            if (path.startswith('/logout') or
                    path.startswith('/unique') or
                    path.startswith('/choice') or
                    path.startswith('/admin') or
                    path.startswith('/welcome') or
                    path.startswith('/base/user-logout') or
                    path.startswith('/base/user-info') or
                    path.startswith('/base/user-perm') or
                    path.startswith('/base/user-reset-pass')):
                return None
        urls = request.session.get('urls')
        if urls:
            for url in urls:
                if path.startswith(url):
                    return None

        return JsonResponse({'success': False, 'message': http_403_error})


class HackHostMiddleware:
    def __init__(self):
        pass

    def process_request(self, request):
        if 'HTTP_HOST' in request.META:
            host = request.META['HTTP_HOST']
            domain, port = split_domain_port(host)
            if domain in ['111.11.84.251', '111.11.84.252']:
                request.META['HTTP_HOST'] = domain


class JsonResponse(HttpResponse):
    def __init__(self, data):
        self.json = data
        HttpResponse.__init__(self)


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return '%04d-%02d-%02d %02d:%02d:%02d' % (obj.year, obj.month, obj.day, obj.hour, obj.minute, obj.second)
        return json.JSONEncoder.default(self, obj)
