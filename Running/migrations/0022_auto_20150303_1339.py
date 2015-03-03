# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0021_auto_20150303_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorship',
            name='max_amount',
            field=models.FloatField(default=9223372036854775807, null=True, verbose_name=b'Max Amount'),
            preserve_default=True,
        ),
    ]
