# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-12-07 00:13
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=250)),
                ('album_title', models.CharField(max_length=500)),
                ('genre', models.CharField(max_length=100)),
                ('album_logo', models.FileField(upload_to='')),
                ('is_favorite', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RFId',
            fields=[
                ('rf_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('in_date', models.DateField(default=datetime.date.today)),
                ('mfr_firm', models.CharField(blank=True, max_length=50)),
                ('expire_yn', models.BooleanField(default=False)),
                ('expire_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RFIdDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('out_firm', models.CharField(blank=True, max_length=50)),
                ('out_date', models.DateField(default=datetime.date.today)),
                ('rf_id_state', models.CharField(default='납품', max_length=4)),
                ('in_date', models.DateField(blank=True, null=True)),
                ('message', models.CharField(blank=True, max_length=100, null=True)),
                ('RFId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.RFId')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_title', models.CharField(max_length=250)),
                ('audio_file', models.FileField(default='', upload_to='')),
                ('is_favorite', models.BooleanField(default=False)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.Album')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='rfiddet',
            unique_together=set([('RFId', 'out_firm')]),
        ),
    ]
