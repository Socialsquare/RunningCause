# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_remove_user_access_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255, null=True, verbose_name=b'image', blank=True),
        ),
    ]
