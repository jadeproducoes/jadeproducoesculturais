# Generated by Django 2.1.dev20171121171147 on 2017-11-26 19:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0022_projeto_arquivar'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeto',
            name='observacao_projeto',
            field=models.TextField(blank=True, null=True, verbose_name='Observação'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='fase_projeto',
            field=models.CharField(blank=True, choices=[('EL', 'Elaboração'), ('DS', 'Desenvolvido'), ('EV', 'Enviado'), ('AN', 'Em análise'), ('RS', 'Recurso seleção'), ('AP', 'Aprovado'), ('AG', 'Aguardando liberação de recursos'), ('PN', 'Pago, mas não iniciado'), ('PE', 'Em execução'), ('PR', 'Pré-produção'), ('PD', 'Produção'), ('PS', 'Pós-produção'), ('EP', 'Elaborando presteação de contas'), ('PC', 'Prestação de contas entregue'), ('AP', 'Análise prestação de contas'), ('PD', 'Pendência prestação de contas'), ('CL', 'Concluído')], max_length=2, null=True, verbose_name='Fase atual do projeto'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='inicio_desenvolvimento',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data de início do desenvolvimento'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='objeto_contratado',
            field=models.TextField(blank=True, null=True, verbose_name='Objeto do contrato'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='resumo',
            field=models.TextField(blank=True, null=True, verbose_name='Resumo do projeto'),
        ),
    ]