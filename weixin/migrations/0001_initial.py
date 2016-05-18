# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django.utils.timezone
from django.conf import settings
import core.utils.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('open_id', models.CharField(unique=True, max_length=30)),
                ('slug', core.utils.models.AutoSlugField(db_index=False, populate_from='user.username', blank=True)),
                ('location', models.CharField(max_length=75, verbose_name='location', blank=True)),
                ('last_seen', models.DateTimeField(auto_now=True, verbose_name='last seen')),
                ('last_ip', models.GenericIPAddressField(null=True, verbose_name='last ip', blank=True)),
                ('localtimezone', models.CharField(default='UTC', max_length=32, verbose_name='time zone', choices=[('Etc/GMT+12', '(GMT -12:00) Eniwetok, Kwajalein'), ('Etc/GMT+11', '(GMT -11:00) Midway Island, Samoa'), ('Etc/GMT+10', '(GMT -10:00) Hawaii'), ('Pacific/Marquesas', '(GMT -9:30) Marquesas Islands'), ('Etc/GMT+9', '(GMT -9:00) Alaska'), ('Etc/GMT+8', '(GMT -8:00) Pacific Time (US & Canada)'), ('Etc/GMT+7', '(GMT -7:00) Mountain Time (US & Canada)'), ('Etc/GMT+6', '(GMT -6:00) Central Time (US & Canada), Mexico City'), ('Etc/GMT+5', '(GMT -5:00) Eastern Time (US & Canada), Bogota, Lima'), ('America/Caracas', '(GMT -4:30) Venezuela'), ('Etc/GMT+4', '(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz'), ('Etc/GMT+3', '(GMT -3:00) Brazil, Buenos Aires, Georgetown'), ('Etc/GMT+2', '(GMT -2:00) Mid-Atlantic'), ('Etc/GMT+1', '(GMT -1:00) Azores, Cape Verde Islands'), ('UTC', '(GMT) Western Europe Time, London, Lisbon, Casablanca'), ('Etc/GMT-1', '(GMT +1:00) Brussels, Copenhagen, Madrid, Paris'), ('Etc/GMT-2', '(GMT +2:00) Kaliningrad, South Africa'), ('Etc/GMT-3', '(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg'), ('Etc/GMT-4', '(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi'), ('Asia/Kabul', '(GMT +4:30) Afghanistan'), ('Etc/GMT-5', '(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent'), ('Asia/Kolkata', '(GMT +5:30) India, Sri Lanka'), ('Asia/Kathmandu', '(GMT +5:45) Nepal'), ('Etc/GMT-6', '(GMT +6:00) Almaty, Dhaka, Colombo'), ('Indian/Cocos', '(GMT +6:30) Cocos Islands, Myanmar'), ('Etc/GMT-7', '(GMT +7:00) Bangkok, Hanoi, Jakarta'), ('Etc/GMT-8', '(GMT +8:00) Beijing, Perth, Singapore, Hong Kong'), ('Australia/Eucla', '(GMT +8:45) Australia (Eucla)'), ('Etc/GMT-9', '(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk'), ('Australia/North', '(GMT +9:30) Australia (Northern Territory)'), ('Etc/GMT-10', '(GMT +10:00) Eastern Australia, Guam, Vladivostok'), ('Etc/GMT-11', '(GMT +11:00) Magadan, Solomon Islands, New Caledonia'), ('Pacific/Norfolk', '(GMT +11:30) Norfolk Island'), ('Etc/GMT-12', '(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka')])),
                ('is_administrator', models.BooleanField(default=False, verbose_name='administrator status')),
                ('is_moderator', models.BooleanField(default=False, verbose_name='moderator status')),
                ('is_verified', models.BooleanField(default=False, help_text='Designates whether the user has verified his account by email or by other means. Un-select this to let the user activate his account.', verbose_name='verified')),
                ('topic_count', models.PositiveIntegerField(default=0, verbose_name='topic count')),
                ('comment_count', models.PositiveIntegerField(default=0, verbose_name='comment count')),
                ('name', models.CharField(default='\u5c0f\u660e', max_length=30)),
                ('sex', models.CharField(default='0', max_length=1)),
                ('phone_num', models.CharField(max_length=20, null=True, blank=True)),
                ('address', models.CharField(max_length=30, null=True, blank=True)),
                ('picture', models.URLField(null=True, blank=True)),
                ('bonus_range', models.IntegerField(default=0)),
                ('snd_bonus_num', models.IntegerField(default=0)),
                ('rcv_bonus_num', models.IntegerField(default=0)),
                ('snd_bonus_value', models.IntegerField(default=0)),
                ('own_bonus_value', models.IntegerField(default=0)),
                ('own_bonus_detail', models.CharField(max_length=100, null=True, blank=True)),
                ('own_ticket_value', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(default=datetime.datetime(2016, 5, 18, 3, 20, 18, 209234, tzinfo=utc))),
                ('subscribe', models.BooleanField(default=True)),
                ('dining_time', models.DateTimeField(default=datetime.datetime(2016, 5, 18, 3, 20, 18, 209294, tzinfo=utc))),
                ('is_admin', models.BooleanField(default=False)),
                ('latest_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'forum profile',
                'verbose_name_plural': 'forum profiles',
            },
        ),
        migrations.CreateModel(
            name='ConsumerAccountGoods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('consumer', models.ForeignKey(related_name='consumer_goods', to='weixin.Consumer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConsumerSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('consumer', models.ForeignKey(to='weixin.Consumer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiningSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person_num', models.IntegerField(default=0)),
                ('begin_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('over_time', models.DateTimeField(null=True, blank=True)),
                ('total_money', models.FloatField(default=0.0)),
                ('total_bonus', models.IntegerField(default=0)),
                ('total_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DiningTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index_table', models.CharField(unique=True, max_length=3)),
                ('status', models.BooleanField(default=False)),
                ('seats', models.IntegerField(default=4)),
                ('is_private', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RcvBonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_bonus', models.CharField(unique=True, max_length=12)),
                ('bonus_type', models.IntegerField(default=0)),
                ('is_message', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=40, null=True, blank=True)),
                ('is_receive', models.BooleanField(default=False)),
                ('is_refuse', models.BooleanField(default=False)),
                ('content', models.CharField(max_length=300, null=True, blank=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('number', models.IntegerField(default=0)),
                ('total_money', models.FloatField(default=0)),
                ('is_best', models.BooleanField(default=False)),
                ('consumer', models.ForeignKey(blank=True, to='weixin.Consumer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recharge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recharge_value', models.FloatField(default=0.0)),
                ('recharge_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('recharge_type', models.IntegerField(default=0)),
                ('recharge_person', models.ForeignKey(related_name='recharge_set', to='weixin.Consumer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecordRcvBonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_record', models.CharField(unique=True, max_length=12)),
                ('bonus_num', models.IntegerField(default=0)),
                ('record_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('consumer', models.ForeignKey(to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='SndBonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_bonus', models.CharField(unique=True, max_length=12)),
                ('bonus_type', models.IntegerField(default=0)),
                ('to_table', models.CharField(max_length=3, null=True, blank=True)),
                ('to_message', models.CharField(max_length=140, null=True, blank=True)),
                ('title', models.CharField(max_length=40, null=True, blank=True)),
                ('content', models.CharField(max_length=300, null=True, blank=True)),
                ('bonus_num', models.IntegerField(default=0)),
                ('number', models.IntegerField(default=0)),
                ('total_money', models.FloatField(default=0)),
                ('bonus_remain', models.IntegerField(default=0)),
                ('bonus_exhausted', models.IntegerField(default=0)),
                ('is_exhausted', models.BooleanField(default=False)),
                ('is_valid', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('over_time', models.DateTimeField(null=True, blank=True)),
                ('user_time', models.DateTimeField(null=True, blank=True)),
                ('consumer', models.ForeignKey(to='weixin.Consumer')),
                ('session', models.ForeignKey(to='weixin.DiningSession', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_ticket', models.CharField(unique=True, max_length=12)),
                ('ticket_type', models.IntegerField(default=0)),
                ('ticket_value', models.FloatField(default=0.0)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_time', models.DateTimeField(null=True, blank=True)),
                ('is_consume', models.BooleanField(default=False)),
                ('consume_time', models.DateTimeField(null=True, blank=True)),
                ('consumer', models.ForeignKey(related_name='ticket_set', to='weixin.Consumer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VirtualMoney',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='\u4e32\u4e32', unique=True, max_length=40)),
                ('price', models.FloatField(default=1.0)),
                ('unit', models.CharField(default='\u4e32', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='WalletMoney',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_money', models.CharField(unique=True, max_length=12)),
                ('is_valid', models.BooleanField(default=True)),
                ('is_used', models.BooleanField(default=False)),
                ('is_send', models.BooleanField(default=False)),
                ('is_receive', models.BooleanField(default=False)),
                ('consumer', models.ForeignKey(related_name='wallet_set', to='weixin.Consumer', null=True)),
                ('money', models.ForeignKey(to='weixin.VirtualMoney')),
                ('rcv_bonus', models.ForeignKey(related_name='wallet_set', blank=True, to='weixin.RcvBonus', null=True)),
                ('recharge', models.ForeignKey(related_name='wallet_set', to='weixin.Recharge', null=True)),
                ('snd_bonus', models.ForeignKey(related_name='wallet_set', to='weixin.SndBonus', null=True)),
                ('ticket', models.ForeignKey(blank=True, to='weixin.Ticket', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='rcvbonus',
            name='record_rcv_bonus',
            field=models.ForeignKey(blank=True, to='weixin.RecordRcvBonus', null=True),
        ),
        migrations.AddField(
            model_name='rcvbonus',
            name='session',
            field=models.ForeignKey(related_name='rcv_bonus_set', blank=True, to='weixin.DiningSession', null=True),
        ),
        migrations.AddField(
            model_name='rcvbonus',
            name='snd_bonus',
            field=models.ForeignKey(to='weixin.SndBonus'),
        ),
        migrations.AddField(
            model_name='diningsession',
            name='table',
            field=models.ForeignKey(to='weixin.DiningTable'),
        ),
        migrations.AddField(
            model_name='consumersession',
            name='session',
            field=models.ForeignKey(to='weixin.DiningSession', null=True),
        ),
        migrations.AddField(
            model_name='consumeraccountgoods',
            name='good',
            field=models.ForeignKey(to='weixin.VirtualMoney'),
        ),
        migrations.AddField(
            model_name='consumer',
            name='on_table',
            field=models.ForeignKey(blank=True, to='weixin.DiningTable', null=True),
        ),
        migrations.AddField(
            model_name='consumer',
            name='session',
            field=models.ForeignKey(related_name='consumer_set', blank=True, to='weixin.DiningSession', null=True),
        ),
        migrations.AddField(
            model_name='consumer',
            name='user',
            field=models.OneToOneField(related_name='jf', verbose_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
