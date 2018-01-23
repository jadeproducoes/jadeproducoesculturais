# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 02:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0014_auto_20171231_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabelairrf',
            name='ano',
            field=models.PositiveIntegerField(default=2018, validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2018)], verbose_name='Ano base'),
        ),
    ]