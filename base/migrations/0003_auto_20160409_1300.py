# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20160404_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='perm',
            field=models.ManyToManyField(to='base.Permission', verbose_name='\u6743\u9650'),
        ),
    ]
