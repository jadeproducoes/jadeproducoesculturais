# Generated by Django 2.1.dev20171121171147 on 2017-11-26 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0007_unidademedida'),
        ('projeto', '0019_auto_20171125_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='FonteFinanciamento',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='utils.Pessoa')),
                ('tipo_fonte', models.CharField(default='FUP', max_length=3, verbose_name='Tipo da fonte')),
                ('contato_fonte', models.CharField(blank=True, max_length=50, null=True, verbose_name='Contato na fonte')),
            ],
            options={
                'verbose_name': 'Fonte de financiamento',
                'verbose_name_plural': 'Fontes de financiamento',
            },
            bases=('utils.pessoa',),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='edital',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Edital'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='fim_inscricoes',
            field=models.DateField(blank=True, null=True, verbose_name='Data final das inscrições'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='fonte_financiamento',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Fonte de financiamento'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='inicio_inscricoes',
            field=models.DateField(blank=True, null=True, verbose_name='Data de início das inscrições'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='nome_projeto',
            field=models.CharField(max_length=200, unique=True, verbose_name='Nome do projeto'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='url_edital',
            field=models.URLField(blank=True, null=True, verbose_name='Local do edital'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='valor_total',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Valor total (obtido do orçamento)'),
        ),
    ]
