# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Running', '0027_user_greeted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField(default=0, null=True, verbose_name=b'Amount')),
                ('fulfilled', models.BooleanField(default=False, verbose_name=b'Fulfilled?')),
                ('paid', models.BooleanField(default=False, verbose_name=b'Paid?')),
                ('remind_date', models.DateField(default=datetime.date(2015, 4, 12), null=True, verbose_name=b'Remind Date')),
                ('wager_text', models.CharField(default=None, max_length=500, null=True, verbose_name=b'Wager Text')),
                ('runner', models.ForeignKey(related_name='wagers_recieved', to=settings.AUTH_USER_MODEL)),
                ('sponsor', models.ForeignKey(related_name='wagers_given', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='run',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 12), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='run',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 12), verbose_name=b'Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 12), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 12), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
    ]
