from django.db import models
from django.db.models import Sum
from projeto.models import Projeto, FonteFinanciamento
from django.utils import timezone
from utils.models import *
from utils.utilitarios import reticencias
#from pagamento.models import Pagamento

# Create your models here.
class Orcamento(models.Model):
    projeto_associado = models.ForeignKey(Projeto, on_delete=models.CASCADE, null=False)
    descricao_orcamento = models.CharField("Identificação do orçamento", max_length=100, null=True, blank=True)
    #valor_solicitado = models.FloatField("Valor solicitado", null=True, blank=True)
    #valor_concedido = models.FloatField("Valor concedido", null=True, blank=True)
    limite_proponente = models.FloatField("Limite do proponente", null=True, blank=True)
    limite_minimo_divulgacao = models.FloatField("Limite mínimo para divulgação", null=True, blank=True)
    limite_administracao = models.FloatField("Limite máximo para administração", null=True, blank=True)
    percentual_pre_producao = models.FloatField("Limite pré-produção(%)", null=True, blank=True)
    percentual_producao = models.FloatField("Limite produção(%)", null=True, blank=True)
    percentual_pos_producao = models.FloatField("Limite pós-produção", null=True, blank=True)
    percentual_elaboracao_captacao = models.FloatField("Limite elaboração ou captação", null=True, blank=True)
    limite_total = models.FloatField("Valor limite do orçamento", null=True, blank=True)
    orcamento_escolhido = models.BooleanField("Orçamento ativo?", default=False)
    agrega_tipo_despesa = models.BooleanField("Agregar por tipo de despesa?", default=False)
    agrega_fase_projeto = models.BooleanField("Agregar por fase de projeto?", default=False)
    agrega_por_fonte = models.BooleanField("Agregar por fonte de financiamento?", default=False)
    data_criacao_orcamento = models.DateTimeField("Criação do orçamento", null=False, blank=False, default=timezone.now)
    arquivar = models.BooleanField("Arquivar orçamento?", default=False)
    rubricas_ordenadas = models.BooleanField("As Rubricas estão ordenadas?", default=False)

    def __str__(self):
        return 'Projeto: %s - Descrição do orçamento: %s' % (self.projeto_associado.nome_projeto, self.descricao_orcamento)

    class Meta:
        ordering = ["-data_criacao_orcamento"]
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"

    @property
    def rubricas_orcamento(self):
        rubricas = None
        if RubricaOrcamento.objects.filter(orcamento_associado=self).exists():
            rubricas = RubricaOrcamento.objects.filter(orcamento_associado=self)
        return rubricas

    @property
    def nr_itens(self):
        total = 0
        if self.rubricas_orcamento:
            total = self.rubricas_orcamento.count()
        return total

    @property
    def valor_bruto(self):
        total = 0
        rubricas = self.rubricas_orcamento
        if rubricas:
            for rubrica in rubricas:
                total += rubrica.valor_bruto_rubrica
        return total

    @property
    def valor_glosas(self):
        total = 0
        if self.rubricas_orcamento:
            if self.rubricas_orcamento.count() > 0:
                for rubrica in self.rubricas_orcamento:
                    total += (rubrica.valor_da_glosa * rubrica.quantidade)
        return total


    @property
    def valor_liquido(self):
        total = 0
        if self.rubricas_orcamento:
            if self.rubricas_orcamento.count() > 0:
                for rubrica in self.rubricas_orcamento:
                    total += ((rubrica.valor_solicitado - rubrica.valor_da_glosa) * rubrica.quantidade)
        return total

def orcamento_ativo(id_projeto):
    if Orcamento.objects.filter(projeto_associado=Projeto.objects.get(pk=id_projeto), orcamento_escolhido=True).exists():
        return Orcamento.objects.filter(projeto_associado=Projeto.objects.get(pk=id_projeto),orcamento_escolhido=True)[0]
    else:
        return None

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

    def ordem_rubricas(self):
        pass

    orcamento_associado = models.ForeignKey(Orcamento, on_delete=models.CASCADE, null=False)
    identificacao_rubrica = models.CharField("Rubrica", max_length=80, null=True, blank=True)
    descricao_rubrica = models.TextField("Descrição da rubrica", null=False, blank=False)
    numero_rubrica = models.PositiveIntegerField("Ordem", default=0, null=False, blank=False)
    justificativa_rubrica = models.TextField("Justificativa", null=True, blank=True)
    PROVIMENTO = (
        ('PO', 'Proponente'),
        ('TR', 'Terceiros'),
        ('FT', 'Ficha técnica'),
        ('PF', 'Terceiros, pessoa física'),
        ('PJ', 'Terceiros, pessoa jurídica'),
        ('OU', 'Outros')
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
    valor_solicitado = models.DecimalField("Valor unitário R$", max_digits=8, decimal_places=2, null=False, blank=False, default=0)
    valor_da_glosa = models.DecimalField("Valor da glosa R$", max_digits=8, decimal_places=2, null=False, blank=False, default=0)
    quantidade = models.DecimalField("Quantidade", max_digits=8, decimal_places=2, null=False, blank=False, default=1)
    FASE_PROJETO = (
        ('PRE', 'Pré-produção'),
        ('PRO', 'Produção'),
        ('POS', 'Pós-produção')
    )
    fase_projeto = models.CharField("Fase do projeto", max_length=3, null=True, blank=True, choices=FASE_PROJETO)
    fonte_financiamento = models.ForeignKey(FonteFinanciamento, null=True, blank=True, on_delete=models.SET_NULL)
    ativa = models.BooleanField("Rubrica ativa?", null=False, blank=False, default=True)

    @property
    def valor_bruto_rubrica(self):
        return self.valor_solicitado * self.quantidade

    @property
    def valor_liquido_rubrica(self):
        return ((self.valor_solicitado - self.valor_da_glosa) * self.quantidade)

    def __str__(self):
        return self.identificacao_rubrica if self.identificacao_rubrica else reticencias(self.descricao_rubrica, 20)

#        facilitador que eu usei no inicio do desenvolvimento
#        return 'Orçamento: %s - Rubrica: %s' % (
#        self.orcamento_associado.descricao_orcamento, self.identificacao_rubrica)

    class Meta:
        ordering = ["numero_rubrica"]
        verbose_name = "Rubrica"
        verbose_name_plural = "Rubricas"


