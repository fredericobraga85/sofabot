# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 00:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SofaBotApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_pair', models.CharField(max_length=20)),
                ('piggy', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OrderState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statusCode', models.IntegerField(default=0)),
                ('perGain', models.FloatField(default=0)),
                ('actual_price', models.FloatField(default=0)),
                ('buy_value', models.FloatField(default=0)),
                ('sell_value', models.FloatField(default=0)),
                ('state_date', models.DateTimeField(verbose_name=b'date state')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SofaBotApp.Exchange')),
            ],
        ),
    ]
