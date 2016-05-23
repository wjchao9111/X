# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='value',
            field=models.CharField(max_length=200, null=True, verbose_name='\u6743\u9650\u503c', blank=True),
            preserve_default=True,
        ),
    ]
