# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-12-12 07:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0013_auto_20171212_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemin',
            name='message',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='itemout',
            name='message',
            field=models.TextField(null=True),
        ),
    ]
