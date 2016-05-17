# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentBookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_number', models.PositiveIntegerField(default=0)),
                ('topic', models.ForeignKey(to='topic.Topic')),
                ('user', models.ForeignKey(related_name='joy_comment_bookmarks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comment bookmark',
                'verbose_name_plural': 'comments bookmarks',
            },
        ),
        migrations.AlterUniqueTogether(
            name='commentbookmark',
            unique_together=set([('user', 'topic')]),
        ),
    ]
