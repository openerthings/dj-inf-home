# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-12-12 07:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0010_auto_20171211_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.CharField(choices=[('PRO', '제품'), ('MAT', '자재'), ('CON', '소모품')], default='PRO', max_length=3),
        ),
        migrations.AddField(
            model_name='itemin',
            name='message',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='itemout',
            name='message',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='itemin',
            name='in_date',
            field=models.DateField(default=datetime.date.today, help_text='입고일자'),
        ),
    ]