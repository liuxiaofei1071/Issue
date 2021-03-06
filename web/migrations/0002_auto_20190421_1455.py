# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-21 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cron',
            old_name='user',
            new_name='create_user',
        ),
        migrations.RemoveField(
            model_name='cron',
            name='host_list',
        ),
        migrations.AddField(
            model_name='cron',
            name='host_list',
            field=models.ManyToManyField(max_length=200, to='web.Host', verbose_name='执行机器'),
        ),
        migrations.AlterField(
            model_name='cron',
            name='job',
            field=models.CharField(max_length=120, verbose_name='计划'),
        ),
        migrations.AlterField(
            model_name='cron',
            name='note',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='计划描述'),
        ),
    ]
