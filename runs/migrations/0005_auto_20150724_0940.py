# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0004_auto_20150717_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='created_dt',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 24, 7, 40, 49, 484223, tzinfo=utc), auto_now_add=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='run',
            name='source_id',
            field=models.CharField(default=None, max_length=200, null=True, verbose_name=b'Source ID', db_index=True),
        ),
    ]
