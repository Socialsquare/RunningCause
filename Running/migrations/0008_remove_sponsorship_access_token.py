# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0007_user_access_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsorship',
            name='access_token',
        ),
    ]
