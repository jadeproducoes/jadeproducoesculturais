# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 18:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0019_auto_20171231_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formadepagamento',
            name='data_efetivacao',
            field=models.DateField(verbose_name='Data da efetivação'),
        ),
    ]
