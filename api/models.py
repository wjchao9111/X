# -*- coding: utf-8 -*-
from django.db import models

from base.models import User


# Create your models here.
class WxltConfig(models.Model):
    pinid = models.CharField(max_length=50, verbose_name=u'pinid', unique=True)
    accountid = models.CharField(max_length=50, verbose_name=u'AccountId')
    accountpwd = models.CharField(max_length=50, verbose_name=u'AccountPwd')
    des_key = models.CharField(max_length=50, verbose_name=u'des_key')
    dept_user = models.OneToOneField(User, related_name='wxlt_config', verbose_name=u'dept_user')

    def __unicode__(self):
        return u'%s' % self.pinid
