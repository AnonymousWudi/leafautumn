# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leafserver', '0002_auto_20160822_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=10, choices=[(b'Image', '\u56fe\u7247'), (b'News', '\u65b0\u95fb')])),
                ('image', models.CharField(max_length=100)),
                ('ranking', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date_added', models.DateTimeField(default=datetime.datetime(2016, 9, 5, 21, 59, 21, 937000), auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='option',
            name='subject',
        ),
        migrations.DeleteModel(
            name='Option',
        ),
        migrations.AddField(
            model_name='indexpage',
            name='news',
            field=models.ForeignKey(to='leafserver.News'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='subject',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='context',
        ),
        migrations.AddField(
            model_name='subject',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'Subject', '\u95ee\u9898'), (b'Option', '\u9009\u9879')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subject',
            name='content',
            field=models.CharField(default=None, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subject',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 5, 21, 59, 21, 935000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subject',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subject',
            name='is_answer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subject',
            name='subject_content',
            field=models.ForeignKey(related_name='options_content', to='leafserver.Subject', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subject',
            name='subject_type',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'Teach', '\u6587\u5316'), (b'Ritual', '\u793c\u5bbe')]),
            preserve_default=True,
        ),
    ]
