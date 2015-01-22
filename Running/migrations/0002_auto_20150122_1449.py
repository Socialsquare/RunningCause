# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='public_information',
            new_name='is_public',
        ),
    ]
