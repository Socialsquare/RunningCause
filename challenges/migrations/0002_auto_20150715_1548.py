# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import challenges.models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='remind_date',
        ),
        migrations.AddField(
            model_name='challenge',
            name='end_date',
            field=models.DateField(default=challenges.models.end_date_default, verbose_name=b'End Date', db_index=True),
        ),
    ]
