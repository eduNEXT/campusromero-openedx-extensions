# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-23 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration_form', '0003_auto_20181024_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customformfields',
            name='institution',
            field=models.TextField(blank=True, max_length=60, null=True, verbose_name='Institution'),
        ),
    ]
