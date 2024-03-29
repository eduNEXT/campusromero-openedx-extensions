# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-11 15:35
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFormFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_of_birth', models.CharField(choices=[(b'1', b'Enero'), (b'2', b'Febrero'), (b'3', b'Marzo'), (b'4', b'Abril'), (b'5', b'Mayo'), (b'6', b'Junio'), (b'7', b'Julio'), (b'8', b'Agosto'), (b'9', b'Septiembre'), (b'10', b'Octubre'), (b'11', b'Noviembre'), (b'12', b'Diciembre')], max_length=2, verbose_name='Month Of Birth')),
                ('day_of_birth', models.CharField(choices=[(b'1', b'01'), (b'2', b'02'), (b'3', b'03'), (b'4', b'04'), (b'5', b'05'), (b'6', b'06'), (b'7', b'07'), (b'8', b'08'), (b'9', b'09'), (b'10', b'10'), (b'11', b'11'), (b'12', b'12'), (b'13', b'13'), (b'14', b'14'), (b'15', b'15'), (b'16', b'16'), (b'17', b'17'), (b'18', b'18'), (b'19', b'19'), (b'20', b'20'), (b'21', b'21'), (b'22', b'22'), (b'23', b'23'), (b'24', b'24'), (b'25', b'25'), (b'26', b'26'), (b'27', b'27'), (b'28', b'28'), (b'29', b'29'), (b'30', b'30'), (b'31', b'31')], max_length=2, verbose_name='Day Of Birth')),
                ('dni', models.TextField(max_length=30, verbose_name='DNI')),
                ('phone_number', models.CharField(max_length=60, verbose_name='Phone Number')),
                ('institution', models.TextField(max_length=60, verbose_name='Institution')),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
