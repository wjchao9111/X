# -*- coding: utf-8 -*-
from django.db import models

from base.models import Dept, User


# Create your models here.
class Cmpp2Cfg(models.Model):
    stat_choices = (('enabled', u'启用'), ('disabled', u'停用'),)
    sock_source_ip = models.CharField(max_length=50, verbose_name=u'源IP地址')
    sock_source_port = models.IntegerField(verbose_name=u'源端口')
    sock_target_ip = models.CharField(max_length=50, verbose_name=u'目的IP地址')
    sock_target_port = models.IntegerField(verbose_name=u'目的端口')
    sock_accept_ip = models.CharField(max_length=50, verbose_name=u'客户端IP地址')
    cmpp_sp_id = models.CharField(max_length=50, verbose_name=u'企业代码')
    cmpp_src_id = models.CharField(max_length=50, verbose_name=u'服务代码')
    cmpp_status = models.CharField(max_length=50, choices=stat_choices, verbose_name=u'端口状态')
    cmpp_dept = models.OneToOneField(Dept, related_name='filter_cmpp2cfg', verbose_name=u'归属部门')

    def __unicode__(self):
        return u'%s' % self.cmpp_src_id


class WhiteList(models.Model):
    src_id = models.CharField(max_length=50, verbose_name=u'服务代码')
    name = models.CharField(max_length=50, verbose_name=u'名称')

    def __unicode__(self):
        return u'%s' % self.src_id


class Filter(models.Model):
    stat_choices = (('new', u'新建'), ('enabled', u'启用'), ('disabled', u'停用'),)
    name = models.CharField(max_length=50, verbose_name=u'名称')
    text = models.CharField(max_length=1000, verbose_name=u'内容')
    note = models.CharField(max_length=1000, null=True, blank=True, verbose_name=u'审批意见')
    cmpp_cfg = models.ForeignKey(Cmpp2Cfg, related_name='filter_set', verbose_name=u'归属端口')
    regex = models.CharField(max_length=1000, verbose_name=u'正则表达式')
    stat = models.CharField(max_length=50, default='new', choices=stat_choices, verbose_name=u'状态')
    user = models.ForeignKey(User, verbose_name=u'归属用户')

    def __unicode__(self):
        return u'%s' % self.name
