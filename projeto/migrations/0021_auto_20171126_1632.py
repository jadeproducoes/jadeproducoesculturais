# Generated by Django 2.1.dev20171121171147 on 2017-11-26 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0020_auto_20171126_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fontefinanciamento',
            name='tipo_fonte',
            field=models.CharField(choices=[('FUP', 'Fundo público'), ('BAC', 'Banco'), ('EPU', 'Empresa pública'), ('EPR', 'Empresa pivada'), ('PRO', 'Proponente'), ('PAR', 'Particular')], default='FUP', max_length=3, verbose_name='Tipo da fonte'),
        ),
    ]