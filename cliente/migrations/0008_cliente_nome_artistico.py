# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0007_auto_20171125_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='nome_artistico',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome artístico/Fantasia'),
        ),
    ]