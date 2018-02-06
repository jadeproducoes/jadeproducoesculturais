# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-05 21:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0038_auto_20180126_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeto',
            name='inicio_vigencia',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Início da vigência do projeto'),
        ),
        migrations.AddField(
            model_name='projeto',
            name='tempo_maximo_realizacao',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Tempo para realização'),
        ),
    ]
