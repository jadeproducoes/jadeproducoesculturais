# Generated by Django 2.1.dev20171121171147 on 2017-11-25 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_pessoa_pessoa_fisica'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='nome',
            field=models.CharField(max_length=100, unique=True, verbose_name='nome'),
        ),
    ]
