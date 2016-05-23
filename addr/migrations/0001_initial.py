# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=50, verbose_name='\u624b\u673a')),
                ('name', models.CharField(max_length=50, verbose_name='\u59d3\u540d')),
                ('sex', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u6027\u522b', choices=[(b'male', '\u7537'), (b'female', '\u5973')])),
                ('email', models.CharField(max_length=50, null=True, verbose_name='\u90ae\u7bb1', blank=True)),
                ('company', models.CharField(max_length=50, null=True, verbose_name='\u516c\u53f8', blank=True)),
                ('dept', models.CharField(max_length=50, null=True, verbose_name='\u90e8\u95e8', blank=True)),
                ('post', models.CharField(max_length=50, null=True, verbose_name='\u804c\u4f4d', blank=True)),
                ('addr', models.CharField(max_length=50, null=True, verbose_name='\u5730\u5740', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddressFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u6587\u4ef6\u540d')),
                ('file', models.FileField(upload_to=b'addr', max_length=50, verbose_name='\u6587\u4ef6')),
                ('init', models.DateTimeField(auto_now_add=True, verbose_name='\u4e0a\u4f20\u65f6\u95f4')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddressGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('mod', models.CharField(default=b'00', max_length=50, verbose_name='\u6a21\u5f0f', choices=[(b'00', '\u79c1\u4eba'), (b'01', '\u5185\u90e8\u53ea\u8bfb'), (b'02', '\u5185\u90e8\u8bfb\u5199'), (b'11', '\u5168\u90e8\u53ea\u8bfb'), (b'12', '\u5916\u90e8\u53ea\u8bfb'), (b'22', '\u5b8c\u5168\u5f00\u653e')])),
                ('dept', models.ForeignKey(verbose_name='\u5f52\u5c5e\u90e8\u95e8', to='base.Dept')),
                ('user', models.ForeignKey(verbose_name='\u5f52\u5c5e\u7528\u6237', to='base.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='addressfile',
            name='group',
            field=models.ForeignKey(verbose_name='\u5f52\u5c5e\u7ec4', to='addr.AddressGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='addressfile',
            name='user',
            field=models.ForeignKey(verbose_name='\u5f52\u5c5e\u7528\u6237', to='base.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='group',
            field=models.ForeignKey(verbose_name='\u5f52\u5c5e\u7ec4', to='addr.AddressGroup'),
            preserve_default=True,
        ),
    ]
