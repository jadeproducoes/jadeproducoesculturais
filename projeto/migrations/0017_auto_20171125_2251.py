# Generated by Django 2.1.dev20171121171147 on 2017-11-26 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0016_auto_20171125_2250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orcamento',
            options={'ordering': ['-data_criacao_orcamento'], 'verbose_name_plural': 'Projeto associado'},
        ),
    ]