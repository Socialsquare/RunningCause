# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0002_remove_user_public_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='public_information',
            field=models.BooleanField(default=False, verbose_name=b'Info public?'),
            preserve_default=True,
        ),
    ]
