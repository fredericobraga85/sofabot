# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-24 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SofaBotApp', '0007_orderstate_currency_pair'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='currency_default',
            field=models.CharField(default='usd', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exchange',
            name='currency_investing',
            field=models.CharField(default='btc', max_length=20),
            preserve_default=False,
        ),
    ]