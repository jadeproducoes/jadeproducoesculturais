# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-14 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0029_auto_20180114_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meta',
            name='descricao_meta',
            field=models.TextField(verbose_name='Meta'),
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='tarefa',
            field=models.TextField(verbose_name='Tarefa'),
        ),
    ]