# Generated by Django 2.1.dev20171121171147 on 2017-11-25 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_auto_20171125_1736'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='areacultural',
            options={'ordering': ['area_cultural'], 'verbose_name_plural': 'Áreas Culturais'},
        ),
        migrations.AlterModelOptions(
            name='pessoa',
            options={'verbose_name_plural': 'Pessoas'},
        ),
    ]
