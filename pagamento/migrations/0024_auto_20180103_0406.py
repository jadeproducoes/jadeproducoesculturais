# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-03 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0023_auto_20180102_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='pendente',
            field=models.BooleanField(default=True, verbose_name='Pagamento pendente?'),
        ),
    ]
