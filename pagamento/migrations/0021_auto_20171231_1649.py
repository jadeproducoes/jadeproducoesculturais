# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0020_auto_20171231_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formadepagamento',
            name='data_efetivacao',
            field=models.DateField(blank=True, null=True, verbose_name='Data da efetivação'),
        ),
    ]
