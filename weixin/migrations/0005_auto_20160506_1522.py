# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-06 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0004_auto_20160506_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='virtualmoney',
            name='value',
        ),
        migrations.AlterField(
            model_name='virtualmoney',
            name='price',
            field=models.FloatField(default=1.0),
        ),
    ]