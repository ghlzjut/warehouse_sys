# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-16 07:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_manage', '0004_clothout_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothout',
            name='AMOUNT',
            field=models.FloatField(default=0.0),
        ),
    ]
