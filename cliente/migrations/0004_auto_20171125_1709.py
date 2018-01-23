# Generated by Django 2.1.dev20171121171147 on 2017-11-25 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_cliente_area_cultural'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='link',
        ),
        migrations.AddField(
            model_name='cliente',
            name='link_perfil_artistico',
            field=models.URLField(blank=True, null=True, verbose_name='Link fanpage'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='ceac',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='número do CEAC'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='curriculo',
            field=models.URLField(blank=True, null=True, verbose_name='link para o currículo'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='observacoes',
            field=models.TextField(blank=True, null=True, verbose_name='observações'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='portfolio',
            field=models.URLField(blank=True, null=True, verbose_name='link para o portfólio'),
        ),
    ]