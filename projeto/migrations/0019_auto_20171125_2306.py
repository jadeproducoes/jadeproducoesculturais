# Generated by Django 2.1.dev20171121171147 on 2017-11-26 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0018_auto_20171125_2257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projeto',
            options={'ordering': ['-inicio_desenvolvimento'], 'verbose_name': 'Projeto', 'verbose_name_plural': 'Projetos'},
        ),
    ]
