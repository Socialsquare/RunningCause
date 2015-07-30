# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sponsorship.models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('token', models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)),
                ('proposed_sponsorship', models.TextField()),
                ('runner', models.ForeignKey(related_name='sponsorships_requested', to=settings.AUTH_USER_MODEL)),
                ('sponsor', models.ForeignKey(related_name='sponsorships_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.DecimalField(default=0, null=True, verbose_name=b'Rate', max_digits=10, decimal_places=2)),
                ('start_date', models.DateField(auto_now_add=True, null=True, verbose_name=b'Start Date', db_index=True)),
                ('end_date', models.DateField(default=sponsorship.models.get_default_end_date, null=True, verbose_name=b'End Date', db_index=True)),
                ('max_amount', models.DecimalField(default=10000, null=True, verbose_name=b'Max Amount', max_digits=10, decimal_places=2)),
                ('amount_paid', models.DecimalField(default=0, verbose_name=b'Amount Paid', max_digits=10, decimal_places=2)),
                ('runner', models.ForeignKey(related_name='sponsorships_recieved', to=settings.AUTH_USER_MODEL)),
                ('sponsor', models.ForeignKey(related_name='sponsorships_given', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='sponsorrequest',
            name='sponsorship',
            field=models.ForeignKey(to='sponsorship.Sponsorship', null=True),
        ),
    ]
