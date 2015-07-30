# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailInvitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('email', models.EmailField(max_length=254, db_index=True)),
                ('updated_dt', models.DateTimeField(auto_now=True, db_index=True)),
                ('token', models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)),
                ('status', models.CharField(default=b'new', max_length=10, choices=[(b'new', b'new'), (b'accepted', b'accepted'), (b'rejected', b'rejected')])),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
