# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-11-28 12:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='interested',
            new_name='interests',
        ),
    ]
