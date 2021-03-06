# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 17:16
from __future__ import unicode_literals

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0013_remove_rubricaorcamento_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='percentual_producao',
            field=models.FloatField(blank=True, null=True, verbose_name='Limite produção(%)'),
        ),
        migrations.AlterField(
            model_name='rubricaorcamento',
            name='numero_rubrica',
            field=models.PositiveIntegerField(default=builtins.id, verbose_name='Item do orçamento'),
        ),
    ]
