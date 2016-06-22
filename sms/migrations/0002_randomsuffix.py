# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20160409_1300'),
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RandomSuffix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dept', models.OneToOneField(related_name='randomsuffix', verbose_name='\u4f01\u4e1a', to='base.Dept')),
            ],
        ),
    ]
