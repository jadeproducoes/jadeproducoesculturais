# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-15 01:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0031_auto_20180114_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarefa',
            name='data_limite_realizacao',
            field=models.DateField(blank=True, null=True, verbose_name='Data limite'),
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='prioridade',
            field=models.PositiveIntegerField(choices=[(0, 'Alta'), (1, 'Média'), (2, 'Baixa')], default=2, verbose_name='Prioridade'),
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='status',
            field=models.CharField(default='0', max_length=1, verbose_name='Status'),
        ),
    ]
