# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_user_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='image',
        ),
        migrations.AddField(
            model_name='user',
            name='picture',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255, null=True, verbose_name='Picture', blank=True),
        ),
    ]
