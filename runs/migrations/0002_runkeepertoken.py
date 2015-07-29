# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('runs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunkeeperToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_token', models.CharField(max_length=200, null=True, blank=True)),
                ('runner', models.OneToOneField(related_name='runkeeper_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
