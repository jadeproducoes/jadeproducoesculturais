# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-03 00:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0027_auto_20171202_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rubricaorcamento',
            name='quantidade',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=8, verbose_name='Quantidade'),
        ),
        migrations.AlterField(
            model_name='rubricaorcamento',
            name='valor_da_glosa',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Valor da glosa'),
        ),
        migrations.AlterField(
            model_name='rubricaorcamento',
            name='valor_solicitado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Valor unitário'),
        ),
    ]
