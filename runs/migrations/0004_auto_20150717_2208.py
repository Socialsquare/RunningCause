# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0003_auto_20150714_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='recorded_time',
            field=models.DurationField(default=datetime.timedelta),
        ),
    ]
