# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_auto_20150821_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='status',
            field=models.CharField(default=b'active', max_length=10, db_index=True, choices=[(b'active', 'active'), (b'completed', 'completed'), (b'declined', 'declined'), (b'confirmed', 'confirmed'), (b'paid', 'paid')]),
        ),
    ]
