# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance', models.FloatField(default=1, verbose_name=b'Distance')),
                ('start_date', models.DateField(auto_now_add=True, verbose_name=b'Date')),
                ('end_date', models.DateField(auto_now_add=True, verbose_name=b'End Date')),
                ('source', models.CharField(default=b'', max_length=200, verbose_name=b'Source')),
                ('source_id', models.CharField(default=b'', max_length=200, verbose_name=b'Source ID')),
                ('recorded_time', models.TimeField(default=datetime.time)),
                ('runner', models.ForeignKey(related_name='runs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
