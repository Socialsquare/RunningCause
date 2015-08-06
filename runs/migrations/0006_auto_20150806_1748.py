# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0005_auto_20150724_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name=b'End Date'),
        ),
        migrations.AlterField(
            model_name='run',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name=b'Date'),
        ),
    ]
