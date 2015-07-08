# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0036_auto_20150417_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 7, 8), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='run',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 7, 8), verbose_name=b'Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='amount_paid',
            field=models.DecimalField(default=0, verbose_name=b'Amount Paid', max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 8, 8), null=True, verbose_name=b'End Date', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='max_amount',
            field=models.DecimalField(default=10000, null=True, verbose_name=b'Max Amount', max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='rate',
            field=models.DecimalField(default=0, null=True, verbose_name=b'Rate', max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 7, 8), null=True, verbose_name=b'Start Date', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='stripe_customer_id',
            field=models.CharField(default=None, max_length=200, blank=True, null=True, verbose_name=b'Stripe Customer Id', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wager',
            name='amount',
            field=models.DecimalField(default=0, null=True, verbose_name=b'Amount', max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wager',
            name='remind_date',
            field=models.DateField(default=datetime.date(2015, 8, 8), null=True, verbose_name=b'Remind Date'),
            preserve_default=True,
        ),
    ]
