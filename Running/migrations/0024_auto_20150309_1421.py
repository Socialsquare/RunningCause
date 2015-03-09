# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0023_auto_20150306_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='newsletter',
            field=models.BooleanField(default=False, verbose_name=b'Newsletter?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='run',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 9), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='run',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 9), verbose_name=b'Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 9), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 9), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
    ]
