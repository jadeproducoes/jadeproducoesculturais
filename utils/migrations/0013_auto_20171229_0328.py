# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-29 05:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0012_auto_20171228_1729'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pessoa',
            options={'ordering': ['nome'], 'verbose_name': 'Pessoa', 'verbose_name_plural': 'Pessoas'},
        ),
    ]
