from django.db import models
from utils.models import *
from utils.utilitarios import *
from cliente.models import Cliente
from django.utils import timezone
#from orcamento.models import Orcamento

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
        ('EX','Em execução'),
        ('PR','Pré-produção'),
        ('PO','Produção'),
        ('PS','Pós-produção'),
        ('EP','Elaborando presteação de contas'),
        ('PE','Prestação de contas entregue'),
        ('AC','Análise prestação de contas'),
        ('PD','Pendência prestação de contas'),
        ('CL', 'Concluído')
    )
    fase_projeto = models.CharField("Fase atual do projeto", max_length=2, choices=FASE_PROJETO, null=True, blank=True)
    objeto_contratado = models.TextField("Objeto do contrato", null=True, blank=True)
    resumo = models.TextField("Resumo do projeto", null=True, blank=True)
    inicio_desenvolvimento = models.DateField("Data de início do desenvolvimento", null=False, blank=False, default=timezone.now)
    observacao_projeto = models.TextField("Observação", null=True, blank=True)
    arquivar = models.BooleanField("Arquivar?", default=False)

    def __str__(self):
        return self.nome_projeto

    class Meta:
        ordering = ["-inicio_desenvolvimento"]
        verbose_name_plural = "Projetos"
        verbose_name = "Projeto"


class Meta(models.Model):
    descricao_meta = models.TextField("Meta", null=False, blank=False)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return reticencias(self.descricao_meta, 50)

    class Meta:
        verbose_name_plural = "Metas"
        verbose_name = "Meta"


class Tarefa(models.Model):

    PRIORIDADE = ((0,'Alta'), (1,'Média'), (2,'Baixa'))
    STATUS = ((0,'Nenhuma ação realizada'), (1,'Em andamento'), (2,'Concluida'))

    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, null=False, blank=False)
    desricao_tarefa = models.TextField("Descrição da tarefa", null=False, blank=False)
    responsavel = models.ForeignKey(Pessoa, null=True, blank=True, on_delete=models.SET_NULL)
    envolvidos = models.TextField("Envolvidos", null=False, blank=False)
    prioridade = models.PositiveIntegerField("Prioridade", choices=PRIORIDADE, default=2, null=False, blank=False)
    meta = models.ForeignKey(Meta, on_delete=None, blank=True, null=True, verbose_name='Meta associada')
    status = models.PositiveIntegerField("Status", null=False, blank=False, default=0, choices=STATUS)
    data_criacao = models.DateField("Data da criação da tarefa", default=timezone.now, blank=False, null=False)
    data_limite_realizacao = models.DateField("Data limite", blank=True, null=True)
    data_conclusao = models.DateField("Data da conclusão", blank=True, null=True)

    def __str__(self):
        return reticencias(self.desricao_tarefa, 50)

    class Meta:
        ordering = ["data_criacao"]
        verbose_name_plural = "Tarefas"
        verbose_name = "Tarefa"

