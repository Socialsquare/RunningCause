# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('challenges', '0002_auto_20150715_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengeRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('token', models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)),
                ('proposed_challenge', models.TextField()),
                ('status', models.CharField(default=b'new', max_length=10, db_index=True, choices=[(b'new', b'new'), (b'accepted', b'accepted'), (b'rejected', b'rejected')])),
                ('runner', models.ForeignKey(related_name='challenges_requested', to=settings.AUTH_USER_MODEL)),
                ('sponsor', models.ForeignKey(related_name='challenges_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='fulfilled',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='token',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='update_text',
        ),
        migrations.AddField(
            model_name='challenge',
            name='runner_msg',
            field=models.CharField(default=None, max_length=500, null=True, verbose_name=b'Feedback message', blank=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='sponsor_msg',
            field=models.CharField(default=None, max_length=500, null=True, verbose_name=b'Feedback message', blank=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='status',
            field=models.CharField(default=b'new', max_length=10, db_index=True, choices=[(b'new', b'new'), (b'completed', b'completed'), (b'declined', b'declined'), (b'confirmed', b'confirmed'), (b'paid', b'paid')]),
        ),
        migrations.AddField(
            model_name='challengerequest',
            name='challenge',
            field=models.ForeignKey(to='challenges.Challenge', null=True),
        ),
    ]
