# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sponsorship.models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0002_auto_20150929_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=sponsorship.models.get_default_end_date, null=True, verbose_name=b'End Date', db_index=True, blank=True),
        ),
    ]
