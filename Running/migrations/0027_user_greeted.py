# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0026_auto_20150310_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='greeted',
            field=models.BooleanField(default=False, verbose_name=b'Greeted?'),
            preserve_default=True,
        ),
    ]
