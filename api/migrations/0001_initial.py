# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WxltConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pinid', models.CharField(unique=True, max_length=50, verbose_name='pinid')),
                ('accountid', models.CharField(max_length=50, verbose_name='AccountId')),
                ('accountpwd', models.CharField(max_length=50, verbose_name='AccountPwd')),
                ('des_key', models.CharField(max_length=50, verbose_name='des_key')),
                ('dept_user', models.OneToOneField(related_name='wxlt_config', verbose_name='dept_user', to='base.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
