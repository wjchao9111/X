# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='note',
            field=models.CharField(max_length=1000, null=True, verbose_name='\u5ba1\u6279\u610f\u89c1', blank=True),
            preserve_default=True,
        ),
    ]
