# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0018_auto_20150211_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorship',
            name='amount_paid',
            field=models.IntegerField(default=0, verbose_name=b'Amount Paid'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='run',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 2, 13), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='run',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 2, 13), verbose_name=b'Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 13), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 2, 13), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
    ]
