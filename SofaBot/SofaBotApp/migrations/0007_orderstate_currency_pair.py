# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 02:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SofaBotApp', '0006_orderstate_ordernumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstate',
            name='currency_pair',
            field=models.CharField(default='-', max_length=20),
            preserve_default=False,
        ),
    ]