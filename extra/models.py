# -*- coding: utf-8 -*-
from django.db import models

from base.models import User


class SI_Contract(models.Model):
    si_name = models.CharField(max_length=50, db_index=True, verbose_name=u'合作伙伴名称')
    prd_name = models.CharField(max_length=50, db_index=True, verbose_name=u'业务名称')
    tax_rate = models.CharField(max_length=50, verbose_name=u'开票税率')
    si_share = models.CharField(max_length=50, verbose_name=u'分成比例')
    si_contact = models.CharField(max_length=50, verbose_name=u'联系人')
    si_phone = models.CharField(max_length=50, verbose_name=u'联系电话')
    no = models.CharField(max_length=50, db_index=True, verbose_name=u'合同编号')
    name = models.CharField(max_length=50, db_index=True, verbose_name=u'合同名称')
    sign_date = models.DateField(verbose_name=u'签署日期')
    eff_date = models.DateField(verbose_name=u'合同起始日')
    vilid_term = models.CharField(max_length=50, verbose_name=u'合同年限')
    exp_date = models.DateField(verbose_name=u'合同终止日')
    exp_date = models.DateField(verbose_name=u'合同终止日')
    delay_month = models.IntegerField(default=0, verbose_name=u'延期支付月数')
    off_date = models.DateField(null=True, blank=True, verbose_name=u'业务下线日')
    change_log = models.CharField(null=True, blank=True, max_length=500, verbose_name=u'变更记录')
    note = models.CharField(null=True, blank=True, max_length=500, verbose_name=u'备注')
    file = models.FileField(max_length=50, upload_to='extra', verbose_name=u'合同文件')
    user = models.ForeignKey(User, verbose_name=u'产品经理')
    init_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    last_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    def __unicode__(self):
        return u'%s-%s(%s)' % (self.no, self.name, self.si_name)


class SI_Pay(models.Model):
    stat_choices = (('init', u'新建'), ('allot', u'已分配'), ('verify', u'已验证'), ('close', u'已关闭'))
    prd_name = models.CharField(max_length=50, db_index=True, verbose_name=u'业务名称')  # C2
    prd_code = models.CharField(max_length=50, verbose_name=u'业务代码')  # C3
    si_name = models.CharField(max_length=50, db_index=True, verbose_name=u'供应商名')  # C4
    tax_rate = models.CharField(max_length=50, verbose_name=u'税率')  # C5
    tax_add_raw = models.FloatField(verbose_name=u'含税价')  # C6
    tax_del_raw = models.FloatField(verbose_name=u'不含税价')  # C7
    tax_raw = models.FloatField(verbose_name=u'税金')  # C8
    adjust = models.FloatField(verbose_name=u'结算调整额')  # C9
    tax_add = models.FloatField(verbose_name=u'含税价')  # C10
    tax_del = models.FloatField(verbose_name=u'不含税价')  # C11
    tax = models.FloatField(verbose_name=u'税金')  # C12
    tax_compute = models.FloatField(verbose_name=u'计算税金')  # C13
    month = models.CharField(max_length=6, db_index=True, verbose_name=u'结算月份')

    contract = models.ForeignKey(SI_Contract, null=True, blank=True, verbose_name=u'关联合同')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=u'产品经理')
    pay_no = models.CharField(null=True, blank=True, max_length=50, unique=True, verbose_name=u'报账单号')
    package = models.CharField(null=True, blank=True, max_length=50, db_index=True, verbose_name=u'报账批次')
    pay_stat = models.CharField(max_length=50, choices=stat_choices, default='init', db_index=True,
                                verbose_name=u'报帐状态')
    init_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    last_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    allot_time = models.DateTimeField(null=True, blank=True, verbose_name=u'分配时间')
    verify_time = models.DateTimeField(null=True, blank=True, verbose_name=u'验证时间')
    close_time = models.DateTimeField(null=True, blank=True, verbose_name=u'关闭时间')

    def __unicode__(self):
        return u'%s-%s(%s)' % (self.si_name, self.prd_name, self.month)


class SI_Invoice(models.Model):
    si_name = models.CharField(max_length=50, db_index=True, verbose_name=u'供应商名')
    goods = models.CharField(max_length=50, verbose_name=u'货物或应税劳务、服务名称')
    tax_del = models.FloatField(verbose_name=u'不含税价')
    tax_rate = models.CharField(max_length=50, verbose_name=u'税率')
    tax_add = models.FloatField(verbose_name=u'含税总额')
    no = models.CharField(max_length=50, db_index=True, verbose_name=u'增值税专用发票编号')
    code = models.CharField(max_length=50, db_index=True, verbose_name=u'发票代码')
    draw_date = models.DateField(verbose_name=u'开票日期')
    recv_date = models.DateField(verbose_name=u'收票日期')
    pay = models.ForeignKey(SI_Pay, verbose_name=u'报账单')

    def __unicode__(self):
        return u'%s-%s(%s):%s' % (self.pay.si_name, self.pay.prd_name, self.pay.month, self.no)


class SI_EmptyPay(models.Model):
    pay_no = models.CharField(null=True, blank=True, max_length=50, unique=True, verbose_name=u'报账单号')
    user = models.ForeignKey(User, verbose_name=u'操作员')

    def __unicode__(self):
        return u'%s' % (self.pay_no)
