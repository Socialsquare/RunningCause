# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0006_auto_20150127_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_token',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'Access token'),
            preserve_default=True,
        ),
    ]
