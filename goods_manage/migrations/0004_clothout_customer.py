# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-11 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_manage', '0003_auto_20180504_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothout',
            name='CUSTOMER',
            field=models.CharField(default='', max_length=50),
        ),
    ]