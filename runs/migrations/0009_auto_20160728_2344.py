# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0008_auto_20160728_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='distance',
            field=models.DecimalField(verbose_name='Distance i kilometre', max_digits=6, decimal_places=2),
        ),
    ]
