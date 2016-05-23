# -*- coding: utf-8 -*-
from django.db import models

from base.models import User, Dept


# Create your models here.

class AddressGroup(models.Model):
    mod_choices = (
        ('00', u'私人'), ('01', u'内部只读'), ('02', u'内部读写'), ('11', u'全部只读'), ('12', u'外部只读'), ('22', u'完全开放'),)
    name = models.CharField(max_length=50, verbose_name=u'名称')
    dept = models.ForeignKey(Dept, verbose_name=u'归属部门')
    user = models.ForeignKey(User, verbose_name=u'归属用户')
    mod = models.CharField(max_length=50, choices=mod_choices, default='00', verbose_name=u'模式')

    def __unicode__(self):
        return u'%s' % self.name


class CommonAddress(models.Model):
    sex_choices = (('male', u'男'), ('female', u'女'),)
    group = models.ForeignKey(AddressGroup, verbose_name=u'归属组')
    phone = models.CharField(max_length=50, verbose_name=u'手机')
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    sex = models.CharField(max_length=50, choices=sex_choices, null=True, blank=True, verbose_name=u'性别')
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'邮箱')
    company = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'公司')
    dept = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'部门')
    post = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'职位')
    addr = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'地址')

    def __unicode__(self):
        return u'%s|%s' % (self.name, self.phone)

    class Meta:
        abstract = True


class Address(CommonAddress):
    pass


class AddressFile(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'文件名')
    file = models.FileField(max_length=50, upload_to='addr', verbose_name=u'文件')
    user = models.ForeignKey(User, verbose_name=u'归属用户')
    group = models.ForeignKey(AddressGroup, verbose_name=u'归属组')
    init = models.DateTimeField(auto_now_add=True, verbose_name=u'上传时间')

    def __unicode__(self):
        return u'%s' % self.name
