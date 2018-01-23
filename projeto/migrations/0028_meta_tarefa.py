# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-14 23:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0015_auto_20180102_0023'),
        ('projeto', '0027_auto_20180102_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao_meta', models.TextField(verbose_name='Meta')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projeto.Projeto')),
            ],
            options={
                'verbose_name': 'Meta',
                'verbose_name_plural': 'Metas',
            },
        ),
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarefa', models.TextField(verbose_name='Tarefa')),
                ('envolvidos', models.TextField(verbose_name='Envolvidos')),
                ('prioridade', models.PositiveIntegerField(choices=[('0', 'Alta'), ('1', 'Média'), ('2', 'Baixa')], default=2, verbose_name='Prioridade')),
                ('status', models.CharField(default='S', max_length=1, verbose_name='Status')),
                ('meta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.Meta', verbose_name='Meta associada')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projeto.Projeto')),
                ('responsavel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utils.Pessoa')),
            ],
            options={
                'verbose_name': 'Tarefa',
                'verbose_name_plural': 'Tarefas',
            },
        ),
    ]