# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_html', models.TextField(verbose_name='comment html')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment_fk', models.ForeignKey(verbose_name='original comment', to='comment.Comment')),
            ],
            options={
                'ordering': ['-date', '-pk'],
                'verbose_name': 'comment history',
                'verbose_name_plural': 'comments history',
            },
        ),
    ]
