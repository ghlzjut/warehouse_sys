# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-24 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_manage', '0002_whiteclothinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothpieceinfo',
            name='Remaeks',
            field=models.CharField(default='', max_length=100),
        ),
    ]
