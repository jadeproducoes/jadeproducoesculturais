# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0023_auto_20171126_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='fase_projeto',
            field=models.CharField(blank=True, choices=[('EL', 'Elaboração'), ('DS', 'Desenvolvido'), ('EV', 'Enviado'), ('AN', 'Em análise'), ('RS', 'Recurso seleção'), ('AP', 'Aprovado'), ('AG', 'Aguardando liberação de recursos'), ('PN', 'Pago, mas não iniciado'), ('EX', 'Em execução'), ('PR', 'Pré-produção'), ('PO', 'Produção'), ('PS', 'Pós-produção'), ('EP', 'Elaborando presteação de contas'), ('PE', 'Prestação de contas entregue'), ('AC', 'Análise prestação de contas'), ('PD', 'Pendência prestação de contas'), ('CL', 'Concluído')], max_length=2, null=True, verbose_name='Fase atual do projeto'),
        ),
    ]
