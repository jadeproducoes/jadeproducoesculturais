# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 18:06
from __future__ import unicode_literals

from django.db import migrations, models
import orcamento.models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0021_auto_20171202_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rubricaorcamento',
            name='numero_rubrica',
            field=models.PositiveIntegerField(default=orcamento.models.RubricaOrcamento.ordem_rubricas, verbose_name='Ordenamentos'),
        ),
    ]
