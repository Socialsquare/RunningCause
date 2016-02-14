# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_auto_20160213_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='end_date',
            field=models.DateField(verbose_name=b'End Date', db_index=True),
        ),
    ]
