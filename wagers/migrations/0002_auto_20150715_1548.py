# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagers.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wager',
            name='remind_date',
        ),
        migrations.AddField(
            model_name='wager',
            name='end_date',
            field=models.DateField(default=wagers.models.end_date_default, verbose_name=b'End Date', db_index=True),
        ),
    ]
