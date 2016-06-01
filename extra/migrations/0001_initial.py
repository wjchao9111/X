# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20160409_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='SI_Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('si_name', models.CharField(max_length=50, verbose_name='\u5408\u4f5c\u4f19\u4f34\u540d\u79f0', db_index=True)),
                ('prd_name', models.CharField(max_length=50, verbose_name='\u4e1a\u52a1\u540d\u79f0', db_index=True)),
                ('tax_rate', models.CharField(max_length=50, verbose_name='\u5f00\u7968\u7a0e\u7387')),
                ('si_share', models.CharField(max_length=50, verbose_name='\u5206\u6210\u6bd4\u4f8b')),
                ('si_contact', models.CharField(max_length=50, verbose_name='\u8054\u7cfb\u4eba')),
                ('si_phone', models.CharField(max_length=50, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('no', models.CharField(max_length=50, verbose_name='\u5408\u540c\u7f16\u53f7', db_index=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u5408\u540c\u540d\u79f0', db_index=True)),
                ('sign_date', models.DateField(verbose_name='\u7b7e\u7f72\u65e5\u671f')),
                ('eff_date', models.DateField(verbose_name='\u5408\u540c\u8d77\u59cb\u65e5')),
                ('vilid_term', models.CharField(max_length=50, verbose_name='\u5408\u540c\u5e74\u9650')),
                ('exp_date', models.DateField(verbose_name='\u5408\u540c\u7ec8\u6b62\u65e5')),
                ('delay_month', models.IntegerField(default=0, verbose_name='\u5ef6\u671f\u652f\u4ed8\u6708\u6570')),
                ('off_date', models.DateField(null=True, verbose_name='\u4e1a\u52a1\u4e0b\u7ebf\u65e5', blank=True)),
                ('change_log', models.CharField(max_length=500, null=True, verbose_name='\u53d8\u66f4\u8bb0\u5f55', blank=True)),
                ('note', models.CharField(max_length=500, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('file', models.FileField(upload_to=b'extra', max_length=50, verbose_name='\u5408\u540c\u6587\u4ef6')),
                ('init_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('user', models.ForeignKey(verbose_name='\u4ea7\u54c1\u7ecf\u7406', to='base.User')),
            ],
        ),
        migrations.CreateModel(
            name='SI_EmptyPay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pay_no', models.CharField(max_length=50, unique=True, null=True, verbose_name='\u62a5\u8d26\u5355\u53f7', blank=True)),
                ('user', models.ForeignKey(verbose_name='\u64cd\u4f5c\u5458', to='base.User')),
            ],
        ),
        migrations.CreateModel(
            name='SI_Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('si_name', models.CharField(max_length=50, verbose_name='\u4f9b\u5e94\u5546\u540d', db_index=True)),
                ('goods', models.CharField(max_length=50, verbose_name='\u8d27\u7269\u6216\u5e94\u7a0e\u52b3\u52a1\u3001\u670d\u52a1\u540d\u79f0')),
                ('tax_del', models.FloatField(verbose_name='\u4e0d\u542b\u7a0e\u4ef7')),
                ('tax_rate', models.CharField(max_length=50, verbose_name='\u7a0e\u7387')),
                ('tax_add', models.FloatField(verbose_name='\u542b\u7a0e\u603b\u989d')),
                ('no', models.CharField(max_length=50, verbose_name='\u589e\u503c\u7a0e\u4e13\u7528\u53d1\u7968\u7f16\u53f7', db_index=True)),
                ('code', models.CharField(max_length=50, verbose_name='\u53d1\u7968\u4ee3\u7801', db_index=True)),
                ('draw_date', models.DateField(verbose_name='\u5f00\u7968\u65e5\u671f')),
                ('recv_date', models.DateField(verbose_name='\u6536\u7968\u65e5\u671f')),
            ],
        ),
        migrations.CreateModel(
            name='SI_Pay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prd_name', models.CharField(max_length=50, verbose_name='\u4e1a\u52a1\u540d\u79f0', db_index=True)),
                ('prd_code', models.CharField(max_length=50, verbose_name='\u4e1a\u52a1\u4ee3\u7801')),
                ('si_name', models.CharField(max_length=50, verbose_name='\u4f9b\u5e94\u5546\u540d', db_index=True)),
                ('tax_rate', models.CharField(max_length=50, verbose_name='\u7a0e\u7387')),
                ('tax_add_raw', models.FloatField(verbose_name='\u542b\u7a0e\u4ef7')),
                ('tax_del_raw', models.FloatField(verbose_name='\u4e0d\u542b\u7a0e\u4ef7')),
                ('tax_raw', models.FloatField(verbose_name='\u7a0e\u91d1')),
                ('adjust', models.FloatField(verbose_name='\u7ed3\u7b97\u8c03\u6574\u989d')),
                ('tax_add', models.FloatField(verbose_name='\u542b\u7a0e\u4ef7')),
                ('tax_del', models.FloatField(verbose_name='\u4e0d\u542b\u7a0e\u4ef7')),
                ('tax', models.FloatField(verbose_name='\u7a0e\u91d1')),
                ('tax_compute', models.FloatField(verbose_name='\u8ba1\u7b97\u7a0e\u91d1')),
                ('month', models.CharField(max_length=6, verbose_name='\u7ed3\u7b97\u6708\u4efd', db_index=True)),
                ('pay_no', models.CharField(max_length=50, unique=True, null=True, verbose_name='\u62a5\u8d26\u5355\u53f7', blank=True)),
                ('package', models.CharField(db_index=True, max_length=50, null=True, verbose_name='\u62a5\u8d26\u6279\u6b21', blank=True)),
                ('pay_stat', models.CharField(default=b'init', max_length=50, verbose_name='\u62a5\u5e10\u72b6\u6001', db_index=True, choices=[(b'init', '\u65b0\u5efa'), (b'allot', '\u5df2\u5206\u914d'), (b'verify', '\u5df2\u9a8c\u8bc1'), (b'close', '\u5df2\u5173\u95ed')])),
                ('init_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('allot_time', models.DateTimeField(null=True, verbose_name='\u5206\u914d\u65f6\u95f4', blank=True)),
                ('verify_time', models.DateTimeField(null=True, verbose_name='\u9a8c\u8bc1\u65f6\u95f4', blank=True)),
                ('close_time', models.DateTimeField(null=True, verbose_name='\u5173\u95ed\u65f6\u95f4', blank=True)),
                ('contract', models.ForeignKey(verbose_name='\u5173\u8054\u5408\u540c', blank=True, to='extra.SI_Contract', null=True)),
                ('user', models.ForeignKey(verbose_name='\u4ea7\u54c1\u7ecf\u7406', blank=True, to='base.User', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='si_invoice',
            name='pay',
            field=models.ForeignKey(verbose_name='\u62a5\u8d26\u5355', to='extra.SI_Pay'),
        ),
    ]
