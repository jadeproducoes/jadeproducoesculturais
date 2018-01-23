# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 23:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0049_auto_20180116_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rubricaorcamento',
            name='provimento',
            field=models.CharField(blank=True, choices=[('PO', 'Proponente'), ('FT', 'Ficha técnica'), ('PF', 'Terceiros, pessoa física'), ('PJ', 'Terceiros, pessoa jurídica'), ('OU', 'Outros')], max_length=2, null=True, verbose_name='Provimento'),
        ),
    ]