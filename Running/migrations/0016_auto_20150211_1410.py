# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0015_auto_20150211_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorship',
            name='sponsor',
            field=models.ForeignKey(related_name='sponsorships_given', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
