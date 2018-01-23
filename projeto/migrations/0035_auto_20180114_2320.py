# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-15 01:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0034_auto_20180114_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefa',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'Nenhuma ação realizada'), (1, 'Em andamento'), (2, 'Concluida')], default=0, verbose_name='Status'),
        ),
    ]