# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cmpp2Cfg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sock_source_ip', models.CharField(max_length=50, verbose_name='\u6e90IP\u5730\u5740')),
                ('sock_source_port', models.IntegerField(verbose_name='\u6e90\u7aef\u53e3')),
                ('sock_target_ip', models.CharField(max_length=50, verbose_name='\u76ee\u7684IP\u5730\u5740')),
                ('sock_target_port', models.IntegerField(verbose_name='\u76ee\u7684\u7aef\u53e3')),
                ('sock_accept_ip', models.CharField(max_length=50, verbose_name='\u5ba2\u6237\u7aefIP\u5730\u5740')),
                ('cmpp_sp_id', models.CharField(max_length=50, verbose_name='\u4f01\u4e1a\u4ee3\u7801')),
                ('cmpp_src_id', models.CharField(max_length=50, verbose_name='\u670d\u52a1\u4ee3\u7801')),
                ('cmpp_status', models.CharField(max_length=50, verbose_name='\u7aef\u53e3\u72b6\u6001', choices=[(b'enabled', '\u542f\u7528'), (b'disabled', '\u505c\u7528')])),
                ('cmpp_dept', models.OneToOneField(related_name='filter_cmpp2cfg', verbose_name='\u5f52\u5c5e\u90e8\u95e8', to='base.Dept')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('text', models.CharField(max_length=1000, verbose_name='\u5185\u5bb9')),
                ('note', models.CharField(max_length=1000, verbose_name='\u7528\u9014')),
                ('regex', models.CharField(max_length=1000, verbose_name='\u6b63\u5219\u8868\u8fbe\u5f0f')),
                ('stat', models.CharField(default=b'new', max_length=50, verbose_name='\u72b6\u6001', choices=[(b'new', '\u65b0\u5efa'), (b'enabled', '\u542f\u7528'), (b'disabled', '\u505c\u7528')])),
                ('cmpp_cfg', models.ForeignKey(related_name='filter_set', verbose_name='\u5f52\u5c5e\u7aef\u53e3', to='filter.Cmpp2Cfg')),
                ('user', models.ForeignKey(verbose_name='\u5f52\u5c5e\u7528\u6237', to='base.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WhiteList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('src_id', models.CharField(max_length=50, verbose_name='\u670d\u52a1\u4ee3\u7801')),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
