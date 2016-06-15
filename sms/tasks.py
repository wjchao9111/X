# -*- coding: utf-8 -*-
from __future__ import absolute_import

import xlrd
from celery import shared_task
from django.db import transaction

from X.tools import get_random_num
from X.tools import lazy_loader_const
from X.tools.log import log
from addr.models import AddressGroup
from sms.models import MsgSend, SendTask


class TaskLoader:
    def __init__(self, task):
        self.task = task
        self.sms_list = []
        self.sms_pos = 0
        self.sms_size = 0
        self.prepare()
        self.random_number = '4' + get_random_num(str_len=3)

    def prepare(self):
        if self.task.type in ['default', 'quick']:
            no_list = []
            no_list += self.get_no_list_from_phones()
            no_list += self.get_no_list_from_groups()
            no_list += self.get_no_list_from_file()
            self.sms_list = self.get_sms_list_from_no_list(no_list)
        if self.task.type in ['dynamic']:
            self.sms_list = self.get_sms_list_from_file()
        self.sms_size = len(self.sms_list)

    def fetch_msg(self, count):
        msg_list = []
        for i in range(count):
            if self.sms_pos < self.sms_size:
                sms = self.sms_list[self.sms_pos]
                msg = self.get_msg(sms[0], sms[1])
                msg_list.append(msg)
                self.sms_pos += 1
        return msg_list

    def get_no_list_from_phones(self):
        task = self.task
        no_list = []
        if task.phones:
            no_list += task.phones.split(',')
        return no_list

    def get_no_list_from_groups(self):
        task = self.task
        no_list = []
        if task.groups:
            grp_list = task.groups.split(',')
            for grp in AddressGroup.objects.filter(id__in=grp_list):
                no_list += [addr.phone for addr in grp.address_set.all()]
        return no_list

    def get_no_list_from_file(self):
        task = self.task
        no_list = []
        if task.file:
            book = xlrd.open_workbook(task.file.path)
            sheet = book.sheets()[0]
            rows = sheet.nrows
            cols = sheet.ncols
            for row in range(1, rows):
                row_data = sheet.row_values(row)
                if row_data:
                    phone = self.get_excel_value(row_data[0])
                    no_list.append(phone)
        return no_list

    def get_sms_list_from_file(self):
        task = self.task
        sms_list = []
        if task.file:
            book = xlrd.open_workbook(task.file.path)
            sheet = book.sheets()[0]
            rows = sheet.nrows
            cols = sheet.ncols
            key_data = sheet.row_values(0)
            key_list = []
            for col in range(cols):
                key_list.append(self.get_excel_value(key_data[col]))
            for row in range(1, rows):
                row_data = sheet.row_values(row)
                if row_data:
                    value_list = []
                    for col in range(cols):
                        value_list.append(self.get_excel_value(row_data[col]))
                    phone = self.get_excel_value(row_data[0])
                    content = self.get_msg_content(key_list, value_list)
                    sms_list.append([phone, content])
        return sms_list

    def get_sms_list_from_no_list(self, no_list):
        content = self.task.content
        return [[no, content] for no in no_list]

    def get_msg(self, phone, content=None):
        task = self.task
        if content == None:
            content = task.content
        msg = MsgSend(
            registered_delivery=task.type != 'quick' and 1 or 0,
            valid_time=task.ending,
            at_time=task.timing,
            src_id=task.suffix,
            dest_terminal_id=phone,
            msg_content=content,
            msg_user=task.user,
            msg_task=task,
        )
        msg.msg_count = get_msg_count(msg)
        if msg.msg_count > 1:
            msg.src_id += self.random_number
        return msg

    def get_excel_value(self, val):
        if type(val) == float:
            if val == int(val):
                return str(int(val))
            else:
                return val
        return val

    def get_msg_content(self, key_list, value_list):
        content = self.task.content
        for i in range(len(key_list)):
            content = content.replace('%' + key_list[i] + '%', unicode(value_list[i]))
        return content


@lazy_loader_const
def get_user_cmpp2cfg(user):
    return user.dept.root.cmpp2cfg


def get_msg_count(msg):
    u_content = msg.msg_content
    try:
        u_sign_zh = get_user_cmpp2cfg(msg.msg_user).cmpp_sign_zh
    except:
        u_sign_zh = u''
    if type(u_content) == str:
        u_content = u_content.decode('utf8')
    if type(u_sign_zh) == str:
        u_sign_zh = u_sign_zh.decode('utf8')

    u_len = len(u_content) + len(u_sign_zh) + 2
    if u_len < 70:
        return 1
    else:
        return int((u_len + 67 - 1) / 67)


def send_task_prepare_sync(task, bulk_size=100, pack_size=20):
    success = False
    try:
        with transaction.atomic():
            loader = TaskLoader(task)
            msg_count = loader.sms_size
            id_list = []
            while True:
                msg_list = loader.fetch_msg(100)
                if msg_list:
                    for msg in msg_list:
                        msg.save()
                        id_list.append(msg.id)
                else:
                    break
            task.stat = 'pre.end'
            task.count = msg_count
            task.save()
            success = True
            return msg_count, id_list
    finally:
        if not success:
            task.stat = 'pre.fail'
            task.save()


@shared_task
def send_task_prepare(task_id):
    task = SendTask.objects.get(id=task_id)
    success = False
    try:
        with transaction.atomic():
            loader = TaskLoader(task)
            msg_count = loader.sms_size
            id_list = []
            log('SEND_TASK_PREPARE', 'ID:%s,MSG_COUNT_ALL:%s' % (task.id, msg_count), 'celery', 'debug')
            count_1 = 0
            while True:
                msg_list = loader.fetch_msg(100)
                if msg_list:
                    MsgSend.objects.bulk_create(msg_list)
                else:
                    break
                count_1 += len(msg_list)
                log('SEND_TASK_PREPARE', 'ID:%s,MSG_COUNT_DONE:%s' % (task.id, count_1), 'celery', 'debug')

            task.stat = 'pre.end'
            task.count = msg_count
            task.save()
            success = True
    except:
        log('SEND_TASK_PREPARE', 'ID:%s' % (task.id), 'celery', 'error')
        if not success:
            task.stat = 'pre.fail'
            task.save()
