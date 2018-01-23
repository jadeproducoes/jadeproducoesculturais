# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-15 00:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0030_auto_20180114_2116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tarefa',
            options={'ordering': ['data_criacao'], 'verbose_name': 'Tarefa', 'verbose_name_plural': 'Tarefas'},
        ),
        migrations.AddField(
            model_name='tarefa',
            name='data_conclusao',
            field=models.DateField(blank=True, null=True, verbose_name='Data da conclusão'),
        ),
        migrations.AddField(
            model_name='tarefa',
            name='data_criacao',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data da criação da tarefa'),
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='prioridade',
            field=models.CharField(choices=[('0', 'Alta'), ('1', 'Média'), ('2', 'Baixa')], default='2', max_length=1, verbose_name='Prioridade'),
        ),
    ]
