# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class Dept(models.Model):
    stat_choices = (('normal', u'正常'), ('disabled', u'禁用'),)
    type_choices = (('system', u'系统'), ('company', u'公司'), ('dept', u'部门'),)
    type = models.CharField(max_length=50, choices=type_choices, verbose_name=u'类型')
    # deptId=models.CharField(max_length=50,verbose_name=u'编码',unique=True)
    name = models.CharField(max_length=50, verbose_name=u'名称')
    stat = models.CharField(max_length=50, choices=stat_choices, verbose_name=u'状态')
    parent = models.ForeignKey('self', related_name='dept_son_set', null=True, blank=True, verbose_name=u'归属')
    root = models.ForeignKey('self', related_name='dept_leaf_set', null=True, blank=True, verbose_name=u'祖先')
    path = models.CharField(max_length=50, verbose_name=u'完整路径')

    def __unicode__(self):
        return u'%s' % self.name

    def set_path(self):
        old_path = self.path
        new_path = self.parent and self.parent.path + '.' + str(self.id) or str(self.id)
        if old_path != new_path:
            self.path = new_path
            self.save()
        for dept in self.dept_son_set.all():
            dept.set_path()


class Permission(models.Model):
    stat_choices = (('normal', u'正常'), ('disabled', u'禁用'),)
    type_choices = (('menu', u'菜单'), ('ajax', u'URL'),)
    type = models.CharField(max_length=50, choices=type_choices, verbose_name=u'类型')
    code = models.CharField(max_length=50, verbose_name=u'编码', unique=True)
    name = models.CharField(max_length=50, verbose_name=u'名称')
    value = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'权限值')
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'描述')
    stat = models.CharField(max_length=50, choices=stat_choices, verbose_name=u'状态')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上级权限')

    def __unicode__(self):
        return u'%s|%s' % (self.code, self.name)


class Role(models.Model):
    stat_choices = (('normal', u'正常'), ('disabled', u'禁用'),)
    type_choices = (('super', u'超级管理员'), ('admin', u'管理员'), ('user', u'用户'),)
    type = models.CharField(max_length=50, choices=type_choices, default='user', verbose_name=u'编码')
    name = models.CharField(max_length=50, verbose_name=u'名称')
    stat = models.CharField(max_length=50, choices=stat_choices, verbose_name=u'状态')
    perm = models.ManyToManyField(Permission, verbose_name=u'权限')
    dept = models.ForeignKey(Dept, related_name='dept_role_set', verbose_name=u'角色')

    def __unicode__(self):
        return u'%s' % self.name


class User(models.Model):
    stat_choices = (('normal', u'正常'), ('disabled', u'禁用'),)
    priority_choices = ((5, u'高'), (7, u'中'), (9, u'低'),)
    code = models.CharField(max_length=50, verbose_name=u'帐号', unique=True)
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    pwd = models.CharField(max_length=50, verbose_name=u'密码')
    phone = models.CharField(max_length=50, verbose_name=u'手机号码')
    email = models.CharField(max_length=50, verbose_name=u'电子邮件')
    priority = models.IntegerField(default=9, choices=priority_choices, verbose_name=u'优先级')
    stat = models.CharField(max_length=50, choices=stat_choices, verbose_name=u'用户状态')
    dept = models.ForeignKey(Dept, related_name='dept_user_set', verbose_name=u'归属部门')
    role = models.ForeignKey(Role, related_name='role_user_set', verbose_name=u'角色')
    admin = models.OneToOneField(Dept, related_name='admin_user', null=True, blank=True, verbose_name=u'管理单位')
    suffix = models.CharField(max_length=50, default='', verbose_name=u'后缀')

    def __unicode__(self):
        return u'%s|%s' % (self.name, self.phone)
