# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagers.models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, verbose_name=b'Amount', max_digits=10, decimal_places=2)),
                ('fulfilled', models.BooleanField(default=False, verbose_name=b'Fulfilled?')),
                ('paid', models.BooleanField(default=False, verbose_name=b'Paid?')),
                ('remind_date', models.DateField(default=wagers.models.remind_date_default, verbose_name=b'Remind Date', db_index=True)),
                ('wager_text', models.CharField(default=b'', max_length=500, verbose_name=b'Wager Text')),
                ('update_text', models.CharField(default=None, max_length=500, null=True, verbose_name=b'Update Text', blank=True)),
                ('status', models.CharField(default=b'n', max_length=1, choices=[(b'n', b'new'), (b'a', b'accepted'), (b'r', b'rejected')])),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('runner', models.ForeignKey(related_name='wagers_recieved', to=settings.AUTH_USER_MODEL)),
                ('sponsor', models.ForeignKey(related_name='wagers_given', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
