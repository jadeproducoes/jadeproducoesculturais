# Generated by Django 2.1.dev20171121171147 on 2017-11-26 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orcamento',
            options={'ordering': ['-data_criacao_orcamento'], 'verbose_name_plural': 'Orçamentos'},
        ),
    ]