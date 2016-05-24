# -*- coding: utf-8 -*-
from __future__ import absolute_import

import xlrd
from celery import shared_task
from django.db import transaction

from X.tools.model import get_object
from addr.models import Address, AddressFile


@shared_task
def addr_file_process(file_id):
    file = AddressFile.objects.get(id=file_id)
    with transaction.atomic():
        book = xlrd.open_workbook(file.file.path)
        sheet = book.sheets()[0]
        rows = sheet.nrows
        cols = sheet.ncols
        for row in range(1, rows):
            row_data = sheet.row_values(row)
            if row_data:
                addr = Address(
                    name=row_data[1],
                    phone=type(row_data[0]) == float and str(int(row_data[0])) or row_data[0],
                    sex=row_data[2] in {u'男': 'male', u'女': 'female'} and {u'男': 'male', u'女': 'female'}[
                        row_data[2]] or row_data[2],
                    email=row_data[3],
                    company=row_data[4],
                    dept=row_data[5],
                    post=row_data[6],
                    addr=row_data[7],
                    group_id=file.group_id
                )
                obj = get_object(Address, phone=addr.phone, group_id=addr.group_id)
                if obj: addr.id = obj.id
                addr.save()
