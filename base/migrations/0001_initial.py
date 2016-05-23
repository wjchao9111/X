# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, verbose_name='\u7c7b\u578b', choices=[(b'system', '\u7cfb\u7edf'), (b'company', '\u516c\u53f8'), (b'dept', '\u90e8\u95e8')])),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('stat', models.CharField(max_length=50, verbose_name='\u72b6\u6001', choices=[(b'normal', '\u6b63\u5e38'), (b'disabled', '\u7981\u7528')])),
                ('path', models.CharField(max_length=50, verbose_name='\u5b8c\u6574\u8def\u5f84')),
                ('parent', models.ForeignKey(related_name='dept_son_set', verbose_name='\u5f52\u5c5e', blank=True, to='base.Dept', null=True)),
                ('root', models.ForeignKey(related_name='dept_leaf_set', verbose_name='\u7956\u5148', blank=True, to='base.Dept', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, verbose_name='\u7c7b\u578b', choices=[(b'menu', '\u83dc\u5355'), (b'ajax', 'URL')])),
                ('code', models.CharField(unique=True, max_length=50, verbose_name='\u7f16\u7801')),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('value', models.CharField(max_length=50, null=True, verbose_name='\u6743\u9650\u503c', blank=True)),
                ('note', models.CharField(max_length=200, null=True, verbose_name='\u63cf\u8ff0', blank=True)),
                ('stat', models.CharField(max_length=50, verbose_name='\u72b6\u6001', choices=[(b'normal', '\u6b63\u5e38'), (b'disabled', '\u7981\u7528')])),
                ('parent', models.ForeignKey(verbose_name='\u4e0a\u7ea7\u6743\u9650', blank=True, to='base.Permission', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'user', max_length=50, verbose_name='\u7f16\u7801', choices=[(b'super', '\u8d85\u7ea7\u7ba1\u7406\u5458'), (b'admin', '\u7ba1\u7406\u5458'), (b'user', '\u7528\u6237')])),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('stat', models.CharField(max_length=50, verbose_name='\u72b6\u6001', choices=[(b'normal', '\u6b63\u5e38'), (b'disabled', '\u7981\u7528')])),
                ('dept', models.ForeignKey(related_name='dept_role_set', verbose_name='\u89d2\u8272', to='base.Dept')),
                ('perm', models.ManyToManyField(to='base.Permission', null=True, verbose_name='\u6743\u9650', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=50, verbose_name='\u5e10\u53f7')),
                ('name', models.CharField(max_length=50, verbose_name='\u59d3\u540d')),
                ('pwd', models.CharField(max_length=50, verbose_name='\u5bc6\u7801')),
                ('phone', models.CharField(max_length=50, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('email', models.CharField(max_length=50, verbose_name='\u7535\u5b50\u90ae\u4ef6')),
                ('priority', models.IntegerField(default=9, verbose_name='\u4f18\u5148\u7ea7', choices=[(5, '\u9ad8'), (7, '\u4e2d'), (9, '\u4f4e')])),
                ('stat', models.CharField(max_length=50, verbose_name='\u7528\u6237\u72b6\u6001', choices=[(b'normal', '\u6b63\u5e38'), (b'disabled', '\u7981\u7528')])),
                ('suffix', models.CharField(default=b'', max_length=50, verbose_name='\u540e\u7f00')),
                ('admin', models.OneToOneField(related_name='admin_user', null=True, blank=True, to='base.Dept', verbose_name='\u7ba1\u7406\u5355\u4f4d')),
                ('dept', models.ForeignKey(related_name='dept_user_set', verbose_name='\u5f52\u5c5e\u90e8\u95e8', to='base.Dept')),
                ('role', models.ForeignKey(related_name='role_user_set', verbose_name='\u89d2\u8272', to='base.Role')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
