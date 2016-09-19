# -*- coding: utf-8 -*-
import base64
import datetime
import os
import re
import zipfile

import xlrd
from django.db.models import Count, Max, Sum
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from django.utils.http import urlquote
from hubarcode.code128 import Code128Encoder

from X.settings import BASE_DIR
from X.tools.middleware import JsonResponse
from X.tools.model import object_list, auto_filter, json_success
from X.tools.storage import TempFile
from extra.models import SI_Contract, SI_Pay, SI_EmptyPay, SI_Invoice
from extra.verify import model_filter


def si_contract_download(request, id):
    si_contract = model_filter(request, SI_Contract.objects.all()).get(id=id)
    response = FileResponse(si_contract.file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s.%s"' % (
        urlquote(unicode(si_contract).encode('utf8'), safe='()'), si_contract.file.name.split('.')[-1])
    return response


def get_month_end(year, month, delay_month):
    month -= delay_month
    month += 1
    while month < 1:
        year -= 1
        month += 12
    while month > 12:
        year += 1
        month -= 12
    next_month = datetime.date(year, month, 1)
    month_end = next_month - datetime.timedelta(days=1)
    return month_end


def get_contract_by_pay(si_pay):
    year = int(si_pay.month[:4])
    month = int(si_pay.month[4:])

    contract_list = SI_Contract.objects.filter(
        si_name__in=[si_pay.si_name, si_pay.si_name.replace('VSP', '')],
        prd_name=si_pay.prd_name,
        # eff_date__lte=month_end,
        # exp_date__gt=month_end
    ).order_by("-eff_date")
    for contract in contract_list:
        month_end = get_month_end(year, month, contract.delay_month)
        if contract.eff_date <= month_end and contract.exp_date > month_end:
            return contract
    return None


def si_pay_allot(si_pay):
    si_contract = get_contract_by_pay(si_pay)
    if si_contract:
        si_pay.contract = si_contract
        si_pay.allot_time = datetime.datetime.now()
        si_pay.pay_stat = 'allot'
        si_pay.user = si_contract.user
        si_pay.save()
        return si_contract
    return None


def si_pay_upload(request):
    obj = request.json.get('object')
    data = obj.get('file').read()
    tempfile = TempFile()
    tempfile.write_and_save(data)
    wb = xlrd.open_workbook(tempfile.path)
    ws = wb.sheet_by_name(u'省级集团客户业务分SI结算表')
    month = None
    count = 0
    for rowx in range(100):
        if ws.cell(rowx, 0).value.startswith(u'开始周期: '):
            month = re.findall(r'\d{6}', ws.cell(rowx, 0).value)[0]
            break
    for rowx in range(rowx + 1, 100):
        if ws.cell(rowx, 0).value == u'石家庄':
            break
    for rowx in range(rowx, 100):
        if not ws.cell(rowx, 1).value:
            break
        try:
            si_pay = SI_Pay.objects.get(prd_name=ws.cell(rowx, 1).value, si_name=ws.cell(rowx, 3).value, month=month)
        except:
            si_pay = SI_Pay()
        si_pay.prd_name = ws.cell(rowx, 1).value
        si_pay.prd_code = str(int(ws.cell(rowx, 2).value))
        si_pay.si_name = ws.cell(rowx, 3).value
        si_pay.tax_rate = str(int(ws.cell(rowx, 4).value * 100)) + '%'
        si_pay.tax_add_raw = ws.cell(rowx, 5).value
        si_pay.tax_del_raw = ws.cell(rowx, 6).value
        si_pay.tax_raw = ws.cell(rowx, 7).value
        si_pay.adjust = ws.cell(rowx, 12).value  # 8
        si_pay.tax_add = ws.cell(rowx, 13).value  # 9
        si_pay.tax_del = ws.cell(rowx, 14).value  # 10
        si_pay.tax = ws.cell(rowx, 15).value  # 11
        si_pay.tax_compute = ws.cell(rowx, 16).value  # 12
        si_pay.month = month
        if not si_pay.user:
            si_pay.user_id = request.session.get('user').get('id')
        si_pay.save()
        count += 1
        if si_pay.pay_stat == 'init':
            si_pay_allot(si_pay)
    tempfile.close()
    return JsonResponse({'success': True, 'message': u'成功上传%s份报账单' % count})


def si_pay_attach(request, si_pay_id):
    si_pay = model_filter(request, SI_Pay.objects.all()).get(id=si_pay_id)
    if si_pay.pay_stat == 'init':
        si_contract = si_pay_allot(si_pay)
        if si_contract:
            return JsonResponse({'success': True, 'message': u'已关联合同：' + unicode(si_contract)})
        else:
            return JsonResponse({'success': False, 'message': u'没有匹配的合同'})
    else:
        return JsonResponse({'success': False, 'message': u'已关联其他合同'})


@object_list
@auto_filter
def si_pay_list(request, stat='all', si_contract_id=None):
    qs = SI_Pay.objects.all()
    if stat != 'all':
        qs = qs.filter(pay_stat=stat)
    if si_contract_id:
        qs = qs.filter(contract_id=si_contract_id)
    return qs


def si_pay_verify(request, si_pay_id):
    si_pay = model_filter(request, SI_Pay.objects.all()).get(id=si_pay_id)
    if si_pay.pay_stat != 'allot':
        return JsonResponse({'success': False, 'message': u'报账单的状态是已分配的才允许执行该操作！'})

    tax_del_sum = 0
    tax_add_sum = 0
    for si_invoice in si_pay.si_invoice_set.all():
        tax_del_sum += si_invoice.tax_del
        tax_add_sum += si_invoice.tax_add
        if si_invoice.tax_rate != si_pay.tax_rate:
            return JsonResponse({'success': False, 'message': u'发票%s税率与报表不一致！' % (si_invoice.no)})
            # if si_invoice.si_name not in [si_pay.si_name, si_pay.si_name.replace('VSP', '')]:
            #    return JsonResponse({'success': False, 'message': u'发票%s供应商名称与报表不一致！' % (si_invoice.no)})
    if tax_del_sum != si_pay.tax_del:
        return JsonResponse({'success': False, 'message': u'发票不含税价合计与报表不一致！'})
    if abs(tax_add_sum - si_pay.tax_add) > 0.2:
        return JsonResponse({'success': False, 'message': u'发票含税价合计与报表差异过大！'})
    if len(SI_EmptyPay.objects.all()) == 0:
        return JsonResponse({'success': False, 'message': u'空报账单号码资源不足，请联系部门报帐员！'})

    si_emptypay = SI_EmptyPay.objects.all()[0]
    si_pay.pay_no = si_emptypay.pay_no
    si_emptypay.delete()

    si_pay.pay_stat = 'verify'
    si_pay.verify_time = datetime.datetime.now()
    si_pay.save()
    return JsonResponse({'success': True, 'message': u'验证发票成功，可打印黏贴单！'})


def si_pay_print(request, si_pay_id):
    si_pay = model_filter(request, SI_Pay.objects.all()).get(id=si_pay_id)
    if si_pay.pay_stat not in ['verify', 'close']:
        return render(request, "echo.html", {'message': u'报账单的状态是已验证的才允许执行该操作！'})

    tempfile = TempFile()
    img = Code128Encoder(si_pay.pay_no,
                         options={'ttf_font': os.path.join(BASE_DIR, 'X', 'static', 'lib', 'FreeMonoBold.ttf')
                             , 'ttf_fontsize': 26, "bottom_border": 12, 'height': 120, 'label_border': 0}
                         ).save(tempfile.path, bar_width=2)
    base64_img = base64.b64encode(tempfile.read_and_close())
    tempfile.close()
    return render(request, "si_pay_print.html", {'pay_name': si_pay, 'base64_img': base64_img})


def si_pay_close(request, si_pay_id):
    si_pay = model_filter(request, SI_Pay.objects.all()).get(id=si_pay_id)
    if si_pay.pay_stat != 'verify':
        return JsonResponse({'success': False, 'message': u'报账单的状态是已验证的才允许执行该操作！'})

    si_pay.pay_stat = 'close'
    si_pay.close_time = datetime.datetime.now()
    si_pay.save()
    return JsonResponse({'success': True, 'message': u'确认接收发票，报账单状态变为已关闭！'})


def si_pay_package_rest(request):
    package = request.json.get('object').get('package')
    si_pay_list = model_filter(request, SI_Pay.objects.all().filter(pay_stat='close', package__isnull=True))
    for si_pay in si_pay_list:
        si_pay.package = package
        si_pay.save()
    return JsonResponse({'success': True, 'message': u'报帐批次%s新建成功，报账单数量%s！' % (package, si_pay_list.count())})


@object_list
def si_pay_package_list(request):
    return model_filter(request, SI_Pay.objects.all().filter(pay_stat='close')) \
        .values('package').annotate(Max('id'), Count('id')).order_by('-id__max')


def si_pay_package_print(request, package, template):
    si_pay_list = model_filter(request, SI_Pay.objects.all().filter(pay_stat='close', package=package)).order_by('id')
    month_list = [month['month'] for month in si_pay_list.values('month').distinct().order_by('month')]
    min_report = dict(si_pay_list.aggregate(Sum('tax_add')), si_pay_list=si_pay_list,
                      month_range='%s-%s' % (month_list[0], month_list[-1]))

    month_report_list = []
    for month in month_list:
        si_pay_list = model_filter(request, SI_Pay.objects.all().filter(month=month)).order_by('id')

        month_report_list.append(
            dict(
                si_pay_list.aggregate(
                    Sum('tax_add'), Sum('tax_del'), Sum('tax'), Sum('adjust'), Sum('tax_add_raw'),
                    Sum('tax_del_raw'), Sum('tax_raw'), Sum('tax_compute')
                ), si_pay_list=si_pay_list, month=month
            )
        )
    return render(request, 'si_report_print.%s.html' % template, {
        'min_report': min_report, 'month_report_list': month_report_list, 'month_list': month_list
    })


def si_pay_package_download(request, package):
    tempdir = TempFile()
    tempfile = TempFile()
    zfile = zipfile.ZipFile(tempfile.path, 'w', zipfile.ZIP_DEFLATED)
    os.mkdir(tempdir.path)

    si_pay_list = model_filter(request, SI_Pay.objects.all().filter(pay_stat='close', package=package)).order_by('id')
    for si_pay in si_pay_list:
        os.mkdir(os.path.join(tempdir.path, si_pay.pay_no))
        # 合同
        contract_name = ("%s.%s" % (unicode(si_pay.contract), si_pay.contract.file.name.split('.')[-1]))
        file_path = os.path.join(tempdir.path, si_pay.pay_no, contract_name).encode('utf8')
        open(file_path, 'wb').write(si_pay.contract.file.read())
        zfile.write(file_path, file_path.replace(tempdir.path, ''))
        os.remove(file_path)
        # 发票
        file_path = os.path.join(tempdir.path, si_pay.pay_no, u'增值税专用发票交接登记表.xls').encode('utf8')
        open(file_path, 'w').write(
            unicode(get_template(
                'si_invoice_print.html'
            ).render(
                Context({'si_invoice_list': si_pay.si_invoice_set.all()})
            )).encode('utf8')
        )
        zfile.write(file_path, file_path.replace(tempdir.path, ''))
        os.remove(file_path)

        os.rmdir(os.path.join(tempdir.path, si_pay.pay_no))

    # 合同
    file_path = os.path.join(tempdir.path, u'合作业务报帐合同清单.xls').encode('utf8')
    open(file_path, 'w').write(
        unicode(get_template(
            'si_contract_print.html'
        ).render(
            Context({'si_contract_list': SI_Contract.objects.all().filter(
                id__in=[si_pay.contract_id for si_pay in si_pay_list])})
        )).encode('utf8')
    )
    zfile.write(file_path, file_path.replace(tempdir.path, ''))
    os.remove(file_path)

    os.rmdir(tempdir.path)
    zfile.close()

    zdata = tempfile.read_and_close()
    tempfile.close()
    response = HttpResponse(zdata)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % package
    return response


@object_list
@auto_filter
def si_invoice_list(request, si_pay_id=None):
    qs = SI_Invoice.objects.all()
    if si_pay_id:
        qs = qs.filter(pay_id=si_pay_id)
    return qs


# 内部使用
def si_emptypay_save(request, pay_no):
    if model_filter(request, SI_EmptyPay.objects.all()).filter(pay_no=pay_no):
        return None
    if model_filter(request, SI_Pay.objects.all()).filter(pay_no=pay_no):
        return None
    si_emptypay = SI_EmptyPay()
    si_emptypay.pay_no = pay_no
    si_emptypay.user_id = request.session.get('user').get('id')
    si_emptypay.save()


@json_success
def si_emptypay_insert(request):
    pay_no = request.json.get('object').get('pay_no')
    no_list = pay_no.split(',')
    first_no = no_list[0]
    si_emptypay_save(request, first_no)

    for no in no_list[1:]:
        si_emptypay_save(request, first_no[:len(no) * -1] + no)
