from django.db import models
from projeto.models import *
from django.utils import timezone
from utils.models import *

# Create your models here.
class Orcamento(models.Model):
    projeto_associado = models.ForeignKey(Projeto, on_delete=models.CASCADE, null=False)
    descricao_orcamento = models.CharField("Particularidade do orçamento", max_length=100, null=True, blank=True)
    valor_solicitado = models.FloatField("Valor solicitado", null=True, blank=True)
    valor_concedido = models.FloatField("Valor concedido", null=True, blank=True)
    limite_proponente = models.FloatField("Limite do proponente", null=True, blank=True)
    limite_minimo_divulgacao = models.FloatField("Limite mínimo para divulgação", null=True, blank=True)
    limite_administracao = models.FloatField("Limite máximo para administração", null=True, blank=True)
    percentual_pre_producao = models.FloatField("Limite pré-produção(%)", null=True, blank=True)
    percentual_producao = models.FloatField("Limite     produção(%)", null=True, blank=True)
    percentual_pos_producao = models.FloatField("Limite pós-produção", null=True, blank=True)
    percentual_elaboracao_captacao = models.FloatField("Limite elaboração ou captação", null=True, blank=True)
    limite_total = models.FloatField("Valor limite do orçamento", null=True, blank=True)
    orcamento_escolhido = models.BooleanField("Orçamento aprovado?", default=False)
    agrega_tipo_despesa = models.BooleanField("Agregar por tipo de despesa?", default=False)
    agrega_fase_projeto = models.BooleanField("Agregar por fase de projeto?", default=False)
    agrega_por_fonte = models.BooleanField("Agregar por fonte de financiamento?", default=False)
    data_criacao_orcamento = models.DateTimeField("Criação do orçamento", null=False, blank=False, default=timezone.now)
    arquivar = models.BooleanField("Arquivar orçamento?", default=False)

    def __str__(self):
        return 'Projeto: %s - Particularidade deste orçamento: %s' % (self.projeto_associado.nome_projeto, self.descricao_orcamento)

    class Meta:
        ordering = ["-data_criacao_orcamento"]
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"

class JutificativaItem(models.Model):
    descricao_justificativa = models.CharField("Justificativa", max_length=60)
    limita_valor = models.BooleanField("Limite de valor?", default=False)
    valor_maximo = models.FloatField("Valor máixmo", default=0)
    codigo_FGV = models.SmallIntegerField("Código da tabela FGV", default=0)
    unidade_medida = models.ForeignKey(UnidadeMedida, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.descricao_justificativa

    class Meta:
        ordering = ["descricao_justificativa"]
        verbose_name = "Justificativa"
        verbose_name_plural = "Justificativas"


class RubricaOrcamento(models.Model):
    orcamento_associado = models.ForeignKey(Orcamento, on_delete=models.CASCADE, null=False)
    identificacao_rubrica = models.CharField("Rubrica", max_length=40, null=True, blank=False)
    descricao_rubrica = models.TextField("Descrição da rubrica", null=False, blank=False)
    numero_rubrica = models.PositiveIntegerField("Item do orçamento", default=0) # precisa resolver isso
    justificativa_rubrica = models.CharField("Justificativa", max_length=200, null=True, blank=True)
    PROVIMENTO = (
        ('PO', 'Proponente'),
        ('FT', 'Ficha técnica'),
        ('PF', 'Terceiros, pessoa física'),
        ('PJ', 'Terceiros, pessoa jurídica')
    )
    provimento = models.CharField("Provimento", max_length=2, null=True, blank=True, choices=PROVIMENTO)
    TIPO_DESPESA = (
        ('EL', 'Elaboração'),
        ('DV', 'Divulgação'),
        ('AD', 'Administrativa'),
        ('PR', 'Produção'),
        ('OU', 'Outros')
    )
    grupo_despesa = models.CharField("Grupo de despesa", max_length=2, null=True, blank=True, choices=TIPO_DESPESA)
    unidade_medida = models.ForeignKey(UnidadeMedida, null=True, blank=True, on_delete=models.SET_NULL)
    valor_solicitado = models.FloatField("Valor unitário", null=False, blank=False, default=0)
    valor_da_glosa = models.FloatField("Valor da glosa", null=False, blank=False, default=0)
    quantidade = models.FloatField("Quantidade", null=False, blank=False, default=1)
    total = models.FloatField("Valor total", null=False, blank=False, default=0)
    FASE_PROJETO = (
        ('PRE', 'Pré-produção'),
        ('PRO', 'Produção'),
        ('POS', 'Pós-produção')
    )
    fase_projeto = models.CharField("Fase do projeto", max_length=3, null=True, blank=True, choices=FASE_PROJETO)
    fonte_financiamento = models.ForeignKey(FonteFinanciamento, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'Orçamento: %s - Rubrica: %s' % (
        self.orcamento_associado.descricao_orcamento, self.identificacao_rubrica)

    class Meta:
        ordering = ["numero_rubrica"]
        verbose_name = "Rubrica"
        verbose_name_plural = "Rubricas"



