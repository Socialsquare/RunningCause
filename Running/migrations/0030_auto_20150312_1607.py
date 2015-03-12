# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0029_wager_update_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wager',
            name='update_text',
            field=models.CharField(default=None, max_length=500, null=True, verbose_name=b'Update Text', blank=True),
            preserve_default=True,
        ),
    ]
