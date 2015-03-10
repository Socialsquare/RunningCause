# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0025_user_stripe_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribed',
            field=models.BooleanField(default=True, verbose_name=b'Subscribed to emails?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='run',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 10), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='run',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 10), verbose_name=b'Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 10), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 10), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='stripe_customer_id',
            field=models.CharField(default=None, max_length=200, null=True, verbose_name=b'Stripe Customer Id'),
            preserve_default=True,
        ),
    ]
