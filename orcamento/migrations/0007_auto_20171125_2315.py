# Generated by Django 2.1.dev20171121171147 on 2017-11-26 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0006_auto_20171125_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='descricao_orcamento',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Particularidade do orçamento'),
        ),
    ]
