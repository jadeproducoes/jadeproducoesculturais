# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-22 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0050_auto_20180116_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rubricaorcamento',
            name='identificacao_rubrica',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Rubrica'),
        ),
    ]
