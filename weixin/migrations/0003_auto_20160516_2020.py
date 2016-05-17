# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0002_auto_20160516_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 16, 12, 20, 0, 329615, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='consumer',
            name='dining_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 16, 12, 20, 0, 329683, tzinfo=utc)),
        ),
    ]
