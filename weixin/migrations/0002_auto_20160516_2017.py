# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 16, 12, 17, 38, 874056, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='consumer',
            name='dining_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 16, 12, 17, 38, 874109, tzinfo=utc)),
        ),
    ]
