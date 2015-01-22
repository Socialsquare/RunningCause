# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0002_auto_20150122_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='sponsorship',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.RemoveField(
            model_name='sponsorship',
            name='active',
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 2, 22), verbose_name=b'End Date'),
            preserve_default=True,
        ),
    ]
