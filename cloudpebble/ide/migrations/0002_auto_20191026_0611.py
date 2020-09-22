# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2019-10-26 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ide', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='theme',
            field=models.CharField(choices=[(b'cloudpebble', b'CloudPebble'), (b'monokai', b'Monokai (Sublime Text)'), (b'blackboard', b'Blackboard (TextMate)'), (b'eclipse', b'Eclipse'), (b'solarized light', b'Solarized (light)'), (b'solarized dark', b'Solarized (dark)'), (b'tomorrow-night-eighties', b'Tomorrow Night (80s)'), (b'3024-night', b'3024 (night)'), (b'xq-dark', b'xq (dark)'), (b'midnight', b'midnight')], default=b'solarized dark', max_length=50, verbose_name='Theme'),
        ),
    ]