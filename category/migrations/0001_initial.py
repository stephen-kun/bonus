# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.utils.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('showimage', models.ImageField(upload_to='categoryimg', null=True, verbose_name='show image', blank=True)),
                ('title', models.CharField(max_length=75, verbose_name='title')),
                ('slug', core.utils.models.AutoSlugField(db_index=False, populate_from='title', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('is_global', models.BooleanField(default=True, help_text='whether the topics will be displayed in the all-categories list.', verbose_name='global')),
                ('is_closed', models.BooleanField(default=False, verbose_name='closed')),
                ('is_removed', models.BooleanField(default=False, verbose_name='removed')),
                ('parent', models.ForeignKey(verbose_name='parent category', blank=True, to='category.Category', null=True)),
            ],
            options={
                'ordering': ['title', 'pk'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
    ]
