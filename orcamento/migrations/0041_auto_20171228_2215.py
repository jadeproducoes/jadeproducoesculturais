# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-29 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0040_auto_20171225_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='descricao_orcamento',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Identificação do orçamento'),
        ),
    ]
