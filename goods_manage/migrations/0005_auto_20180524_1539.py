# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-24 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_manage', '0004_auto_20180524_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothpieceinfo',
            name='REMARKS',
            field=models.CharField(default='-', max_length=100),
        ),
    ]
