# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0022_auto_20171231_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itempagamento',
            name='quantidade',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Quantidade do item'),
        ),
    ]
