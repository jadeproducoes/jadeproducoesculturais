# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-18 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carregaarquivo', '0006_auto_20180118_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcaoarquivo',
            name='sigla_funcao',
            field=models.CharField(default='', max_length=3, verbose_name='Sigla função'),
        ),
    ]