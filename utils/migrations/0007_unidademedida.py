# Generated by Django 2.1.dev20171121171147 on 2017-11-26 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0006_auto_20171125_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnidadeMedida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao_unidade', models.CharField(max_length=20, verbose_name='Unidade de medida')),
            ],
            options={
                'verbose_name': 'Unidade de medida',
                'verbose_name_plural': 'Unidades de medidas',
                'ordering': ['descricao_unidade'],
            },
        ),
    ]
