# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0041_auto_20171228_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='rubricas_ordenadas',
            field=models.BooleanField(default=False, verbose_name='As rubricas já foram ordenadas?'),
        ),
    ]
