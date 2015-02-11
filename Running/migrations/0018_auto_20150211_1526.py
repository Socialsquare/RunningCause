# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0017_auto_20150211_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 11), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='max_amount',
            field=models.IntegerField(default=9223372036854775807, null=True, verbose_name=b'Max Amount'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='rate',
            field=models.FloatField(default=0, null=True, verbose_name=b'Rate'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 2, 11), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
    ]
