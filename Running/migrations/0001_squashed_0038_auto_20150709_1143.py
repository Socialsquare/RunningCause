# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    replaces = [(b'Running', '0001_initial'), (b'Running', '0002_auto_20150122_1449'), (b'Running', '0003_auto_20150122_1929'), (b'Running', '0004_auto_20150122_2009'), (b'Running', '0005_auto_20150123_1350'), (b'Running', '0006_auto_20150127_1330'), (b'Running', '0007_user_access_token'), (b'Running', '0008_remove_sponsorship_access_token'), (b'Running', '0009_auto_20150128_1508'), (b'Running', '0010_auto_20150128_1639'), (b'Running', '0011_auto_20150128_1642'), (b'Running', '0012_auto_20150203_1344'), (b'Running', '0013_auto_20150209_1201'), (b'Running', '0014_auto_20150210_1712'), (b'Running', '0015_auto_20150211_1353'), (b'Running', '0016_auto_20150211_1410'), (b'Running', '0017_auto_20150211_1504'), (b'Running', '0018_auto_20150211_1526'), (b'Running', '0019_auto_20150213_1339'), (b'Running', '0020_auto_20150302_1400'), (b'Running', '0021_auto_20150303_1311'), (b'Running', '0022_auto_20150303_1339'), (b'Running', '0023_auto_20150306_1923'), (b'Running', '0024_auto_20150309_1421'), (b'Running', '0025_user_stripe_customer_id'), (b'Running', '0026_auto_20150310_1356'), (b'Running', '0027_user_greeted'), (b'Running', '0028_auto_20150312_1405'), (b'Running', '0029_wager_update_text'), (b'Running', '0030_auto_20150312_1607'), (b'Running', '0031_auto_20150312_1646'), (b'Running', '0032_auto_20150316_1744'), (b'Running', '0033_auto_20150317_1500'), (b'Running', '0034_auto_20150318_1238'), (b'Running', '0035_auto_20150319_1055'), (b'Running', '0036_auto_20150417_1530'), (b'Running', '0037_auto_20150708_1226'), (b'Running', '0038_auto_20150709_1143')]

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
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
                ('is_public', models.BooleanField(default=False, verbose_name=b'Info public?')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
                ('access_token', models.CharField(default=b'', max_length=200, verbose_name=b'Access token', blank=True)),
                ('newsletter', models.BooleanField(default=False, verbose_name=b'Newsletter?')),
                ('stripe_customer_id', models.CharField(default=None, max_length=200, null=True, verbose_name=b'Stripe Customer Id')),
                ('subscribed', models.BooleanField(default=True, verbose_name=b'Subscribed to emails?')),
                ('greeted', models.BooleanField(default=False, verbose_name=b'Greeted?')),
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
            field=models.ForeignKey(related_name='sponsorships_given', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='run',
            name='runner',
            field=models.ForeignKey(related_name='runs', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='sponsorship',
            name='active',
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 2, 22), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='run',
            name='date',
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 2, 23), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 1, 23), verbose_name=b'Start Date', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 2, 27), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 1, 27), verbose_name=b'Start Date', editable=False),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='sponsorship',
            name='access_token',
        ),
        migrations.AddField(
            model_name='run',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 7, 9), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='run',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 7, 9), verbose_name=b'Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 2, 28), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 1, 28), verbose_name=b'Start Date', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 3), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 2, 3), verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 9), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 2, 9), verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 10), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 2, 10), verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 11), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 2, 11), verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 11), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='max_amount',
            field=models.IntegerField(default=9223372036854775807, null=True, verbose_name=b'Max Amount'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='rate',
            field=models.FloatField(default=0, null=True, verbose_name=b'Rate'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 2, 11), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsorship',
            name='amount_paid',
            field=models.DecimalField(default=0, verbose_name=b'Amount Paid', max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 3, 13), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 2, 13), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 2), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 2), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 3), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 3), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='max_amount',
            field=models.FloatField(default=9223372036854775807, null=True, verbose_name=b'Max Amount'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 6), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 6), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 9), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 9), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 10), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 10), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Wager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, null=True, verbose_name=b'Amount', max_digits=10, decimal_places=2)),
                ('fulfilled', models.BooleanField(default=False, verbose_name=b'Fulfilled?')),
                ('paid', models.BooleanField(default=False, verbose_name=b'Paid?')),
                ('remind_date', models.DateField(default=datetime.date(2015, 8, 9), null=True, verbose_name=b'Remind Date')),
                ('wager_text', models.CharField(default=None, max_length=500, null=True, verbose_name=b'Wager Text')),
                ('runner', models.ForeignKey(related_name='wagers_recieved', to=settings.AUTH_USER_MODEL)),
                ('sponsor', models.ForeignKey(related_name='wagers_given', to=settings.AUTH_USER_MODEL, null=True)),
                ('update_text', models.CharField(default=None, max_length=500, null=True, verbose_name=b'Update Text', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
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
        migrations.AlterField(
            model_name='user',
            name='stripe_customer_id',
            field=models.CharField(default=None, max_length=200, null=True, verbose_name=b'Stripe Customer Id', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 16), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 16), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 17), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 17), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 18), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 18), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 4, 19), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 3, 19), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 5, 17), null=True, verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 4, 17), null=True, verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 8, 8), null=True, verbose_name=b'End Date', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='max_amount',
            field=models.DecimalField(default=10000, null=True, verbose_name=b'Max Amount', max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='rate',
            field=models.DecimalField(default=0, null=True, verbose_name=b'Rate', max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 7, 8), null=True, verbose_name=b'Start Date', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='stripe_customer_id',
            field=models.CharField(default=None, max_length=200, blank=True, null=True, verbose_name=b'Stripe Customer Id', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='end_date',
            field=models.DateField(default=datetime.date(2015, 8, 9), null=True, verbose_name=b'End Date', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 7, 9), null=True, verbose_name=b'Start Date', db_index=True),
            preserve_default=True,
        ),
    ]
