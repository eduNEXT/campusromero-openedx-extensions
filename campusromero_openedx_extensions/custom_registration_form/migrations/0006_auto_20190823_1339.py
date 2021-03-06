# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-08-23 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration_form', '0005_auto_20190410_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customformfields',
            name='dni',
            field=models.TextField(blank=True, max_length=10, null=True, verbose_name='DNI'),
        ),
        migrations.AlterField(
            model_name='customformfields',
            name='institution',
            field=models.TextField(blank=True, default='', max_length=60, null=True, verbose_name='Institution'),
        ),
        migrations.AlterField(
            model_name='customformfields',
            name='phone_number',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Phone Number'),
        ),
    ]
