# Generated by Django 2.1.dev20171121171147 on 2017-11-25 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0004_auto_20171125_1709'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'ordering': ['nome'], 'verbose_name_plural': 'Clientes'},
        ),
    ]