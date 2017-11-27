from django.db import models
from utils.models import *
from cliente.models import Cliente
from django.utils import timezone

# Create your models here.

# Fonte de financiamento
class FonteFinanciamento(Pessoa):
    TIPO_FONTE = (
        ('FUP', 'Fundo público'),
        ('BAC', 'Banco'),
        ('EPU', 'Empresa pública'),
        ('EPR', 'Empresa pivada'),
        ('PRO', 'Proponente'),
        ('PAR', 'Particular')
    )
    tipo_fonte = models.CharField("Tipo da fonte", max_length=3, null=False, choices=TIPO_FONTE, blank=False, default='FUP')
    contato_fonte = models.CharField("Contato na fonte", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Fontes de financiamento"
        verbose_name = "Fonte de financiamento"


# Projetos culturais
class Projeto(models.Model):
    nome_projeto = models.CharField("Nome do projeto", max_length=200, unique=True)
    cliente_projeto = models.ForeignKey(Cliente, on_delete=None, null=True, blank=True)
    area_cultural = models.ForeignKey(AreaCultural, on_delete=None, null=True, blank=True)
    fonte_financiamento = models.CharField("Fonte de financiamento", max_length=40, null=True, blank=True)
    edital = models.CharField("Edital", max_length=50, null=True, blank=True)
    url_edital = models.URLField("Local do edital", null=True, blank=True)
    inicio_inscricoes = models.DateField("Data de início das inscrições", null=True, blank=True)
    fim_inscricoes = models.DateField("Data final das inscrições", null=True, blank=True)
    valor_total = models.FloatField("Valor total (obtido do orçamento)", null=True, blank=True, default=0)
    FASE_PROJETO = (
        ('EL','Elaboração'),
        ('DS','Desenvolvido'),
        ('EV','Enviado'),
        ('AN','Em análise'),
        ('RS','Recurso seleção'),
        ('AP','Aprovado'),
        ('AG','Aguardando liberação de recursos'),
        ('PN','Pago, mas não iniciado'),
        ('PE','Em execução'),
        ('PR','Pré-produção'),
        ('PD','Produção'),
        ('PS','Pós-produção'),
        ('EP','Elaborando presteação de contas'),
        ('PC','Prestação de contas entregue'),
        ('AP','Análise prestação de contas'),
        ('PD','Pendência prestação de contas'),
        ('CL', 'Concluído')
    )
    fase_projeto = models.CharField("Fase atual do projeto", max_length=2, choices=FASE_PROJETO, null=True, blank=True)
    objeto_contratado = models.TextField("Objeto do contrato", null=True, blank=True)
    resumo = models.TextField("Resumo do projeto", null=True, blank=True)
    inicio_desenvolvimento = models.DateField("Data de início do desenvolvimento", null=False, blank=False, default=timezone.now)
    observacao_projeto = models.TextField("Observação", null=True, blank=True)
    arquivar = models.BooleanField("Arquivar projeto?", default=False)

    def __str__(self):
        return self.nome_projeto

    class Meta:
        ordering = ["-inicio_desenvolvimento"]
        verbose_name_plural = "Projetos"
        verbose_name = "Projeto"
