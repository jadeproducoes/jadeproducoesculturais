# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0046_auto_20180102_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='rubricas_ordenadas',
            field=models.BooleanField(default=False, verbose_name='As rubricas estão ordenadas?'),
        ),
    ]