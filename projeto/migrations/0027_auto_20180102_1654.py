# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0026_auto_20171228_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='arquivar',
            field=models.BooleanField(default=False, verbose_name='Arquivar?'),
        ),
    ]
