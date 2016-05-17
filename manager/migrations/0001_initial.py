# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('action', models.IntegerField(default=1)),
                ('source', models.CharField(default='\u7ba1\u7406\u5458\u5145\u503c', max_length=32)),
                ('value', models.FloatField(default=0)),
                ('is_admin', models.BooleanField(default=True)),
                ('consumer', models.ForeignKey(to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='DailyDetailContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(default=0)),
                ('daily_detail', models.ForeignKey(related_name='content_set', to='manager.DailyDetail')),
                ('good', models.ForeignKey(to='weixin.VirtualMoney')),
            ],
        ),
        migrations.CreateModel(
            name='DailyGoodStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charge_number', models.IntegerField(default=0)),
                ('consume_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DailyStatisticsRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('consume_value', models.FloatField(default=0)),
                ('charge_value', models.FloatField(default=0)),
                ('account', models.FloatField(default=0)),
                ('is_admin', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='dailygoodstatistics',
            name='daily_statistics',
            field=models.ForeignKey(related_name='content_set', to='manager.DailyStatisticsRecord'),
        ),
        migrations.AddField(
            model_name='dailygoodstatistics',
            name='good',
            field=models.ForeignKey(to='weixin.VirtualMoney'),
        ),
    ]
