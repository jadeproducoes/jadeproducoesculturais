from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# Classe generica de pessoas fisicas ou juridicas
class Pessoa(models.Model):
    nome = models.CharField("Nome/razão social", max_length=100, null=False, blank=False, unique=True)
    pessoa_fisica = models.BooleanField("Pessoa física?", default=True)
    email = models.EmailField("Email", max_length=150, null=True, blank=True)
    fone1 = models.CharField("Fone (1)", max_length=40, null=True, blank=True)
    fone2 = models.CharField("Fone (2)", max_length=40, null=True, blank=True)
    endereco = models.CharField("endereço completo", max_length=200, null=True, blank=True)
    cpfoucnpj = models.CharField("CPF ou CNPJ", max_length=20, null=True, blank=True)
    identidadeouinscricao = models.CharField("Identidade ou Inscrição Estadual", max_length=30, null=True, blank=True)
    redesocial = models.URLField("Link rede social", null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Pessoas"
        verbose_name = "Pessoa"
        ordering = ["nome"]

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

class TabelaIRRF(models.Model):

    ano = models.PositiveIntegerField("Ano base",blank=False,
                                      validators=[MinValueValidator(2000),MaxValueValidator(datetime.now().year)],
                                      default=datetime.now().year)

    limite_faixa1 = models.DecimalField("Limite isenção", default=0, decimal_places=2, max_digits=8)

    limite_faixa2 = models.DecimalField("Limite 2a faixa", default=0, decimal_places=2, max_digits=8)
    aliquota_faixa2 = models.DecimalField("Aliquota 2a faixa", default=0, decimal_places=2, max_digits=8)
    deducao_faixa2 = models.DecimalField("Dedução 2a faixa", default=0, decimal_places=2, max_digits=8)

    limite_faixa3 = models.DecimalField("Limite 3a faixa", default=0, decimal_places=2, max_digits=8)
    aliquota_faixa3 = models.DecimalField("Aliquota 3a faixa", default=0, decimal_places=2, max_digits=8)
    deducao_faixa3 = models.DecimalField("Dedução 3a faixa", default=0, decimal_places=2, max_digits=8)

    limite_faixa4 = models.DecimalField("Limite 4a faixa", default=0, decimal_places=2, max_digits=8)
    aliquota_faixa4 = models.DecimalField("Aliquota 4a faixa", default=0, decimal_places=2, max_digits=8)
    deducao_faixa4 = models.DecimalField("Dedução 4a faixa", default=0, decimal_places=2, max_digits=8)

    aliquota_faixa5 = models.DecimalField("Aliquota 5a faixa", default=0, decimal_places=2, max_digits=8)
    deducao_faixa5 = models.DecimalField("Dedução 5a faixa", default=0, decimal_places=2, max_digits=8)

    ativa = models.BooleanField("Tabela ativa?", default=True)

    class Meta:
        ordering = ["-ano"]
        verbose_name_plural = "Tabelas de IRRF"
        verbose_name = "Tabela de IRRF"

    def __str__(self):
        tab_ativa = " (Não ativa)"
        if self.ativa:
            tab_ativa = " (Ativa)"
        return str(self.ano) + tab_ativa

class AliquotaISS(models.Model):
    percentual = models.DecimalField("Percentual", decimal_places=2, max_digits=10,
                                          default=0)
    local_cobrança = models.CharField("Local de cobrança", max_length=20, blank=True, null=True)

class AliquotaINSS(models.Model):
    percentual = models.DecimalField("Percentual", decimal_places=2, max_digits=10,
                                          default=0)
    local_cobrança = models.CharField("Observação", max_length=30, blank=True, null=True)


def formaspagamento():
    return (('CH', 'Cheque'), ('DI', 'Dinheiro'),('TR','Transferência'))

def tipocomprovacao():
    return (('NF', 'Nota Fiscal'),
            ('RP', 'RPA Emitida pelo projeto'),
            ('RB','RPA Emitida pelo beneficiário'),
            ('CP', 'Cupom fiscal'))
