# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 04:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0024_auto_20171205_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeto',
            name='percentual_ISS',
            field=models.DecimalField(decimal_places=1, default=0.05, max_digits=3, verbose_name='Percentual ISS'),
        ),
        migrations.AddField(
            model_name='projeto',
            name='precentual_INSS',
            field=models.DecimalField(decimal_places=1, default=0.11, max_digits=4, verbose_name='Percentual INSS'),
        ),
    ]