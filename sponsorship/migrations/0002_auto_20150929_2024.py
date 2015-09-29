# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(null=True, verbose_name=b'Start Date', db_index=True),
        ),
    ]
