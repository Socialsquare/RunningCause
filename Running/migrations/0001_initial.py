# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField(default=0, verbose_name=b'Amount')),
                ('active', models.BooleanField(default=True, verbose_name=b'Active')),
                ('start_date', models.DateField(default=datetime.date(2015, 1, 22), verbose_name=b'Start Date', editable=False)),
                ('end_date', models.DateField(default=datetime.date(2015, 2, 1), verbose_name=b'End date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance', models.FloatField(default=1, verbose_name=b'Distance')),
                ('date', models.DateField(default=datetime.date(2015, 1, 22), verbose_name=b'Date')),
                ('source', models.CharField(default=b'', max_length=200, verbose_name=b'Source')),
                ('source_id', models.CharField(default=b'', max_length=200, verbose_name=b'Source ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.FloatField(default=0, verbose_name=b'Rate')),
                ('start_date', models.DateField(default=datetime.date(2015, 1, 22), verbose_name=b'Start Date', editable=False)),
                ('end_date', models.DateField(default=datetime.date(2015, 2, 19), verbose_name=b'End Date')),
                ('max_amount', models.IntegerField(default=9223372036854775807, verbose_name=b'Max Amount')),
                ('access_token', models.CharField(default=b'', max_length=200, verbose_name=b'Access Token')),
                ('active', models.BooleanField(default=True, verbose_name=b'Active')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_runner', models.BooleanField(default=False, verbose_name=b'Is Runner')),
                ('is_sponsor', models.BooleanField(default=False, verbose_name=b'Is Sponsor?')),
                ('public_information', models.BooleanField(default=False, verbose_name=b'Info public?')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sponsorship',
            name='runner',
            field=models.ForeignKey(related_name='sponsorships_recieved', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsorship',
            name='sponsor',
            field=models.ForeignKey(related_name='sponsorships_given', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='run',
            name='runner',
            field=models.ForeignKey(related_name='runs', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='payment',
            name='sponsorship',
            field=models.ForeignKey(related_name='payments', to='Running.Sponsorship'),
            preserve_default=True,
        ),
    ]
