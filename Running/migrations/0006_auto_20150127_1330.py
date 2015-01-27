# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0005_auto_20150123_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='date',
            field=models.DateField(default=datetime.date(2015, 1, 27), verbose_name=b'Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 2, 27), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 1, 27), verbose_name=b'Start Date', editable=False),
            preserve_default=True,
        ),
    ]
