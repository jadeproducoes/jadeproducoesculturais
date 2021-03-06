# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0024_auto_20171202_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='rubricas_ordenadas',
            field=models.BooleanField(default=False, verbose_name='As rubricas já foram ordenadas'),
        ),
        migrations.AlterField(
            model_name='rubricaorcamento',
            name='numero_rubrica',
            field=models.PositiveIntegerField(default=0, verbose_name='Ordenamento'),
        ),
    ]
