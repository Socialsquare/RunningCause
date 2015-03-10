# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0024_auto_20150309_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stripe_customer_id',
            field=models.IntegerField(default=None, null=True, verbose_name=b'Stripe Customer Id'),
            preserve_default=True,
        ),
    ]
