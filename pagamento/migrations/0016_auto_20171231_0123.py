# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 03:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0015_auto_20171231_0007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formadepagamento',
            options={'verbose_name': 'Forma de Pagamento', 'verbose_name_plural': 'Formas de Pagamento'},
        ),
        migrations.AlterField(
            model_name='formadepagamento',
            name='nr_documento',
            field=models.CharField(max_length=12, null=True, verbose_name='Nr. documento (cheque, transf., etc)'),
        ),
    ]
