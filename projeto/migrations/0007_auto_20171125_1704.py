# Generated by Django 2.1.dev20171121171147 on 2017-11-25 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0006_auto_20171125_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='edital',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='edital'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='fase_projeto',
            field=models.CharField(blank=True, choices=[('EL', 'Elaboração'), ('DS', 'Desenvolvido'), ('EV', 'Enviado'), ('AN', 'Em análise'), ('RS', 'Recurso seleção'), ('AP', 'Aprovado'), ('AG', 'Aguardando liberação de recursos'), ('PN', 'Pago, mas não iniciado'), ('PE', 'Em execução'), ('PR', 'Pré-produção'), ('PD', 'Produção'), ('PS', 'Pós-produção'), ('EP', 'Elaborando presteação de contas'), ('PC', 'Prestação de contas entregue'), ('AP', 'Análise prestação de contas'), ('PD', 'Pendência prestação de contas'), ('CL', 'Concluído')], max_length=2, null=True, verbose_name='fase atual do projeto'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='fim_inscricoes',
            field=models.DateField(blank=True, null=True, verbose_name='data final das inscrições'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='fonte_financiamento',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='fonte de financiamento'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='inicio_inscricoes',
            field=models.DateField(blank=True, null=True, verbose_name='data de início das inscrições'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='objeto_contratado',
            field=models.TextField(blank=True, null=True, verbose_name='objeto do contrato'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='resumo',
            field=models.TextField(blank=True, null=True, verbose_name='resumo do projeto'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='url_edital',
            field=models.URLField(blank=True, null=True, verbose_name='local do edital'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='valor_total',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='valor total (obtido do orçamento)'),
        ),
    ]
