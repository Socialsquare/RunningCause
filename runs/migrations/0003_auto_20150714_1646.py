# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0002_runkeepertoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runkeepertoken',
            name='access_token',
            field=models.CharField(db_index=True, max_length=200, unique=True, null=True, blank=True),
        ),
    ]
