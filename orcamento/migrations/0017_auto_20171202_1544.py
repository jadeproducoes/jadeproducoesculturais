# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0016_auto_20171202_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rubricaorcamento',
            name='numero_rubrica',
            field=models.PositiveIntegerField(default=0, verbose_name='Ordem no orçamento'),
        ),
    ]
