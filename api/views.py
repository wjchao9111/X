# -*- coding: utf-8 -*-
import hashlib
import string
import random
import pickle
import time

import redis

from django.views.decorators.csrf import csrf_exempt

from base.models import User
from X.tools.model import get_object
from X.tools.middleware import JsonResponse
from sms.serv.smstools import get_api_user
from sms.views import get_task, send_task_prepare_sync


# Create your views here.
redis_obj = redis.Redis()


@csrf_exempt
def get_token(request, code):
    timestamp = request.json['timestamp']
    nonce = request.json['nonce']
    signature = request.json['signature']
    user = get_user_by_code(code)
    if user is None:
        return JsonResponse({'success': False, 'error_code': 'User not found or disabled'})
    key = get_key(user)

    if signature != get_sha1([timestamp, nonce, key]):
        return JsonResponse({'success': False, 'error_code': 'Signature validate failed'})
    token = redis_get_token(user)
    if token:
        return JsonResponse({'success': True, 'token': token})
    else:
        return JsonResponse({'success': False, 'error_code': 'The query is too frequent'})


def test(request, key):
    key = get_key_with_len(key)
    timestamp = str(time.time())
    nonce = get_random_str()
    signature = get_sha1([timestamp, nonce, key])
    return JsonResponse({'success': True, 'msg': {'timestamp': timestamp, 'nonce': nonce, 'signature': signature}})


@csrf_exempt
def send_sms(request):
    task_list = request.json.get('task_list')
    if not task_list:
        task_list = []
    j_task = request.json.get('task')
    if j_task:
        task_list.append(j_task)

    token = request.json['token']
    uid = redis_get_uid_by_token(token)
    if uid is None:
        return JsonResponse({'success': False, 'error_code': 'Token validate failed'})
    result_list = []
    # print task_list
    for j_task in task_list:
        task = get_task(j_task)
        task.user_id = uid
        task.save()
        taskcount, id_list = send_task_prepare_sync(task)
        result_list.append({'count': taskcount, 'id_list': id_list})
    return JsonResponse({'success': True, 'result_list': result_list})


@csrf_exempt
def recv_sms(request):
    token = request.json['token']
    uid = redis_get_uid_by_token(token)
    if uid is None:
        return JsonResponse({'success': False, 'error_code': 'Token validate failed'})
    if redis_get_traffic_control(uid):
        redis_set_traffic_control(uid, ex=30)
        return JsonResponse({'success': False, 'error_code': 'The query is too frequent'})
    sms_list = []
    for i in range(100):
        msg = redis_pop_obj('recv_sms', uid)
        if msg is None:
            break
        else:
            sms_list.append(msg)
    if not sms_list:
        redis_set_traffic_control(uid)
    return JsonResponse({'success': True, 'sms_list': sms_list})


@csrf_exempt
def status_report(request):
    token = request.json['token']
    uid = redis_get_uid_by_token(token)
    if uid is None:
        return JsonResponse({'success': False, 'error_code': 'Token validate failed'})
    if redis_get_traffic_control(uid):
        redis_set_traffic_control(uid, ex=30)
        return JsonResponse({'success': False, 'error_code': 'The query is too frequent'})
    sms_list = []
    for i in range(100):
        msg = redis_pop_obj('status_report', uid)
        if msg is None:
            break
        else:
            sms_list.append(msg)
    if not sms_list:
        redis_set_traffic_control(uid)
    return JsonResponse({'success': True, 'sms_list': sms_list})


def redis_push_obj(key, uid, msg, app='api'):
    r = redis_obj
    key = redis_get_key(key, uid, app)
    s_msg = pickle.dumps(msg)
    r.lpush(key, s_msg)
    if not r.ttl(key):
        r.expire(key, 3 * 24 * 3600)


def redis_pop_obj(key, uid, app='api'):
    r = redis_obj
    key = redis_get_key(key, uid, app)
    s_msg = r.rpop(key)
    if s_msg is None:
        return None
    else:
        msg = pickle.loads(s_msg)
        r.expire(key, 3 * 24 * 3600)
        return msg


def redis_get_key(key, param, app='api'):
    return '%s:%s:%s' % (app, key, param)


def redis_get_token(user):
    r = redis_obj
    last_token_key = redis_get_key('last_token', user.id)
    last_token = r.get(last_token_key)
    if last_token and r.get(redis_get_key('token', last_token)):
        return None

    while True:
        token = get_random_str()
        if not r.get(redis_get_key('token', token)):
            break
    r.set(redis_get_key('token', token), user.id)
    r.expire(redis_get_key('token', token), 1800)
    r.set(redis_get_key('last_token', user.id), token)
    r.expire(redis_get_key('last_token', user.id), 1800/10)
    return token


def redis_get_uid_by_token(token):
    r = redis_obj
    uid = r.get(redis_get_key('token', token))
    if uid is None:
        return None
    else:
        return int(uid)


def redis_set_traffic_control(uid, ex=3):
    r = redis_obj
    key = redis_get_key('traffic_control', uid)
    r.set(key, ex)
    r.expire(key, ex)


def redis_get_traffic_control(uid):
    r = redis_obj
    key = redis_get_key('traffic_control', uid)
    return r.get(key)


def get_user_by_code(code):
    user = get_object(User, code=code)
    #if user in get_api_user():
    return user


def get_user_by_id(id):
    user = get_object(User, id=id)
    return user


def get_key(user):
    key = user.pwd
    return get_key_with_len(key)


def get_key_with_len(key, key_len=32):
    pass_len = len(key)
    if pass_len > key_len:
        key = key[:key_len]
    elif pass_len < key_len:
        key += ' ' * (key_len - pass_len)
    return key


def get_sha1(array):
    tmp_array = array
    tmp_array.sort()
    tmp_str = ''.join(tmp_array)
    hash_value = hashlib.sha1(tmp_str).hexdigest()
    return hash_value


def get_random_str(str_len=32):
    rule = string.letters + string.digits
    str = random.sample(rule, str_len)
    return "".join(str)


def get_random_num(str_len=32):
    rule = string.digits
    str = random.sample(rule, str_len)
    return "".join(str)
