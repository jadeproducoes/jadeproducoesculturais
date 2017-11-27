from django.db import models

# Create your models here.

# Classe generica de pessoas fisicas ou juridicas
class Pessoa(models.Model):
    nome = models.CharField("nome", max_length=100, null=False, blank=False, unique=True)
    pessoa_fisica = models.BooleanField("pessoa física", default=True)
    email = models.EmailField("email", max_length=150, null=True, blank=True)
    fone1 = models.CharField("fone (1)", max_length=40, null=True, blank=True)
    fone2 = models.CharField("fone (2)", max_length=40, null=True, blank=True)
    endereco = models.CharField("endereço completo", max_length=200, null=True, blank=True)
    cpfoucnpj = models.CharField("CPF ou CNPJ", max_length=20, null=True, blank=True)
    identidadeouinscricao = models.CharField("Identidade ou Inscrição Estadual", max_length=30, null=True, blank=True)
    redesocial = models.URLField("Link rede social", null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Pessoas"
        verbose_name = "Pessoa"

# Cadastro de areas culturais
class AreaCultural(models.Model):
    area_cultural = models.CharField("área cultural", max_length=30, unique=True)
    sub_area = models.BooleanField(default=False)

    def __str__(self):
        return self.area_cultural

    class Meta:
        ordering = ["area_cultural"]
        verbose_name_plural = "Áreas Culturais"
        verbose_name = "Área Cultural"

class UnidadeMedida(models.Model):
    descricao_unidade = models.CharField("Unidade de medida", max_length=20)

    def __str__(self):
        return self.descricao_unidade

    class Meta:
        ordering = ["descricao_unidade"]
        verbose_name_plural = "Unidades de medidas"
        verbose_name = "Unidade de medida"
