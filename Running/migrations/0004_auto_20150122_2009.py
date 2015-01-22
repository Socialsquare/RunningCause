# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0003_auto_20150122_1929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_runner',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_sponsor',
        ),
    ]
