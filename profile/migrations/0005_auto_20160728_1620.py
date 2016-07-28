# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_auto_20160728_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255, null=True, verbose_name='Billede', blank=True),
        ),
    ]
