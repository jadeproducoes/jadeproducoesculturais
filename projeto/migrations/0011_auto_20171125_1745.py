# Generated by Django 2.1.dev20171121171147 on 2017-11-25 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0010_auto_20171125_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projeto',
            options={'ordering': ['-inicio_desenvolvimento'], 'verbose_name_plural': 'Projetos'},
        ),
    ]
