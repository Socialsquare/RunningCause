# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0030_auto_20150312_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='stripe_customer_id',
            field=models.CharField(default=None, max_length=200, null=True, verbose_name=b'Stripe Customer Id', blank=True),
            preserve_default=True,
        ),
    ]
