# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_auto_20150729_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengerequest',
            name='runner',
            field=models.ForeignKey(related_name='ingoing_challenge_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='challengerequest',
            name='sponsor',
            field=models.ForeignKey(related_name='outgoing_challenge_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
