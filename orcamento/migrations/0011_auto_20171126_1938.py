# Generated by Django 2.1.dev20171121171147 on 2017-11-26 21:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0010_auto_20171126_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='data_criacao_orcamento',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criação do orçamento'),
        ),
    ]