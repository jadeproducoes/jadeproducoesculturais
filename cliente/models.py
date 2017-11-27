from django.db import models
from utils.models import *

# Create your models here.

# Especializa a classe Pessoa como Cliente

class Cliente(Pessoa):
    area_cultural = models.ForeignKey(AreaCultural, on_delete=None, blank=True, null=True)
    ceac = models.CharField("número do CEAC", max_length=4, null=True, blank=True)
    curriculo = models.URLField("link para o currículo", null=True, blank=True)
    portfolio = models.URLField("link para o portfólio", null=True, blank=True)
    link_perfil_artistico = models.URLField("Link fanpage", null=True, blank=True)
    observacoes = models.TextField("observações", null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]
        verbose_name_plural = "Clientes"
        verbose_name = "Cliente"