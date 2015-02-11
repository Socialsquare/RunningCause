# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0016_auto_20150211_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorship',
            name='sponsor',
            field=models.ForeignKey(related_name='sponsorships_given', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
