from django.db import models
from django.utils import timezone
from projeto.models import Projeto
from utils.models import *
from utils.utilitarios import *
from orcamento.models import Orcamento, RubricaOrcamento
from django.db.models import Sum
from decimal import *

# Create your models here.

# Os valores dos pagamentos, para efeito de controle orcamentario, sao calculados pelo bruto
# apenas para efeito de emissao de RPA, no caso de pessoas fisicas, seram calculados os valores
# brutos e liquidos para a formatacao do documento e posterior recolhimento dos impostos

class Pagamento(models.Model):

    id_pessoa = models.ForeignKey(Pessoa, on_delete=None, null=True, blank=False,
                                  verbose_name="Beneficiário")
    id_projeto = models.ForeignKey(Projeto, on_delete=None, null=True, blank=False,
                                   verbose_name="Projeto relacionado")
    id_orcamento = models.ForeignKey(Orcamento, on_delete=None, null=True, blank=False,
                                   verbose_name="Orçamento relacionado")
    cobrar_ISS = models.BooleanField("Cobra ISS?", default=True)
    cobrar_INSS = models.BooleanField("Cobrar INSS?", default=False)
    data_pagamento = models.DateField("Data do pagamento", default=timezone.now)
    pendente = models.BooleanField("Pagamento pendente?", default=True, null=False, blank=False)
    observacoes = models.TextField("Observações", max_length=200, null=True, blank=True)

    def __str__(self):
        return "Beneficiário(a) " + str(self.id_pessoa)

    class Meta:
        ordering = ["-data_pagamento"]
        verbose_name_plural = "Pagamentos"
        verbose_name = "Pagamento"

    @property
    def itens_pagamento(self):
        return ItemPagamento.objects.filter(id_pagamento=self)

    @property
    def lista_itens_pagamento(self):
        str_itens = []
        if self.itens_pagamento:
            str_itens = [str(rubrica) for rubrica in self.itens_pagamento]
        return str_itens

    @property
    def formas_pagamento(self):
        return FormaDePagamento.objects.filter(id_pagamento=self)

    @property
    def lista_formas_pagamento(self):
        str_forma = []
        if self.formas_pagamento:
            str_forma = [str(forma) for forma in self.formas_pagamento]
        return str_forma

    @property
    def formas_comprovacao(self):
        return FormaComprovacao.objects.filter(id_pagamento=self)

    @property
    def lista_formas_comprovacao(self):
        str_forma = []
        if self.formas_comprovacao:
            str_forma = [str(forma) for forma in self.formas_comprovacao]
        return str_forma

    @property
    def valor_bruto_pagamento(self):
        total = ItemPagamento.objects.filter(id_pagamento=self).aggregate(somatorio=Sum('valor_bruto_pagamento'))
        if total['somatorio']:
            valor = total['somatorio']
        else:
            valor = 0.0
        return valor

    @property
    def valores_descontos(self):
        calcula_IR = True
        if self.id_pessoa:
            if not self.id_pessoa.pessoa_fisica:
                calcula_IR = False
                self.cobrar_INSS = False
                self.cobrar_ISS = False

        return calcula_impostos(self.valor_bruto_pagamento, self.cobrar_ISS, self.cobrar_INSS, calcula_IR)

    @property
    def total_descontos(self):
        return self.valores_descontos['Descontos']

    @property
    def valor_liquido(self):
        return self.valores_descontos['Liquido']

    @property
    def valor_ISS(self):
        return self.valores_descontos['ISS']

    @property
    def valor_INSS(self):
        return self.valores_descontos['INSS']

    @property
    def valor_IR(self):
        return self.valores_descontos['IR']

    @property
    def soma_fomas_pagamento(self):
        total = 0
        formas_pagamento = FormaDePagamento.objects.filter(id_pagamento=self)
        if formas_pagamento:
            if formas_pagamento.count() > 0:
                total = formas_pagamento.aggregate(formas=Sum('valor'))['formas']
        return Decimal(total)

    @property
    def soma_formas_comprovacao(self):
        total = 0
        formas_comprovacao = FormaComprovacao.objects.filter(id_pagamento=self)
        if formas_comprovacao:
            if formas_comprovacao.count() > 0:
                total = formas_comprovacao.aggregate(formas=Sum('valor'))['formas']
        return Decimal(total)

    @property
    def pendencias_pagamento(self):
        cor = cores('padrao')
        mensagem = ""
        pendencias = {'existentes':False, 'cor':cor, 'msg':mensagem}

        existem_meios_pagamento = False
        # Pendencia de forma de pagamento e a falta de lancamento da data de comepensacao
        if FormaDePagamento.objects.filter(id_pagamento=self).exists():
            formas_pagamento = FormaDePagamento.objects.filter(id_pagamento=self)
            existem_meios_pagamento = True
            for forma in formas_pagamento:
                if not forma.data_efetivacao:
                    cor = cores('alerta')
                    mensagem = "- Não existe indicação da compensação de um ou mais MEIOS DE PAGAMENTO"
                    break
        else:
            mensagem = "- Não foram indicados os MEIOS DE PAGAMENTO"

        # Pendencia de forma de comprovacao podem gerar situacoes mais graves
        if FormaComprovacao.objects.filter(id_pagamento=self).exists():
            formas_comprovacao = FormaComprovacao.objects.filter(id_pagamento=self)
            for forma in formas_comprovacao:
                if not forma.data_recebimento:
                    cor = cores('alerta')
                    if mensagem != "":
                        mensagem += "\n"
                    mensagem += "- Não existe(m) data(s) de registro(s) de recebimento de um ou mais MEIOS DE COMPROVAÇÃO"
                    break
        else:
            if mensagem != "":
                mensagem += "\n"
            if existem_meios_pagamento:
                cor = cores('critico')
                mensagem += "ATENÇÃO! Apesar de existerem meios de pagamento, não existem MEIOS DE COMPROVAÇÃO"
            else:
                mensagem += "- Não foram indicados MEIOS DE COMPROVAÇÃO"

        if mensagem != "":
            pendencias['existentes'] = True
            pendencias['cor'] = cor
            pendencias['msg'] = mensagem

        return pendencias

class ItemPagamento(models.Model):

    id_pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, null=True, blank=False)
    id_rubrica = models.ForeignKey(RubricaOrcamento, on_delete=None, null=True, blank=False,
                                   verbose_name="Rubrica relacionada")
    quantidade = models.DecimalField("Quantidade do item", decimal_places=2, max_digits=10,
                                          default=0) # informar quantidade deve calcular automaticamente o valor
    valor_bruto_pagamento = models.DecimalField("Valor a pagar (R$)", decimal_places=2, max_digits=10, default=0)  # colocar limites

    @property
    def valor_usado_rubrica(self):
        valor_usado = 0
        if self.id_rubrica is None:
            return None
        else:
            orcamento = self.id_pagamento.id_orcamento
            pagamentos = Pagamento.objects.filter(id_orcamento=orcamento)
            for pagamento in pagamentos:
                if ItemPagamento.objects.filter(id_pagamento=pagamento).exists():
                    itens_pagamento = ItemPagamento.objects.filter(id_pagamento=pagamento)
                    for item in itens_pagamento:
                        if item.id_rubrica == self.id_rubrica:
                            valor_usado += item.valor_bruto_pagamento
                    #rubrica = ItemPagamento.objects.filter(id_rubrica=self.id_rubrica).aggregate(valor_usado=Sum('valor_bruto_pagamento'))
        return valor_usado

    @property
    def saldo_rubrica(self):
        if self.id_rubrica is None:
            return None
        else:
            return (self.id_rubrica.valor_liquido_rubrica - self.valor_usado_rubrica)

class FormaDePagamento(models.Model):
    id_pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, null=True, blank=False)
    forma = models.CharField("Meio de pagamento", max_length=2, null=True, blank=False,
                             choices=formaspagamento(), default='CH')
    nr_documento = models.CharField("Nr. documento (cheque, transf., etc)", max_length=12, null=True, blank=False)
    valor = models.DecimalField("Valor desta forma pagamento (R$)", decimal_places=2, max_digits=10, default=0.0)
    data_emissao = models.DateField("Data da emissão", default=timezone.now)
    data_efetivacao = models.DateField("Data da efetivação", null=True, blank=True)

    def __str__(self):
        op_pagamentos = formaspagamento()
        nr_doc = "nº {}".format(self.nr_documento) if self.nr_documento else ""
        return "{} ".format([(forma) for forma in op_pagamentos if self.forma in forma][0][1]) + nr_doc

    class Meta:
        verbose_name_plural = "Formas de Pagamento"
        verbose_name = "Forma de Pagamento"

    @property
    def meio_pagamento(self):
        meios = formaspagamento()
        nome_meio = ""
        for meio in meios:
            if meio[0] == self.forma:
                nome_meio = meio[1]
        return nome_meio

class FormaComprovacao(models.Model):
    id_pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, null=True, blank=False)
    tipo_comprovacao = models.CharField("Tipo de comprovação", max_length=2, default='NF', null=True, blank=True,
                                        choices=tipocomprovacao())
    nr_doc_comprovacao = models.CharField("Nr documento de comprovação", max_length=15, null=True, blank=False)
    valor = models.DecimalField("Valor do documento(R$)", decimal_places=2, max_digits=10,
                                default=0.0)  # colocar limites
    data_emissao = models.DateField("Data da emissão", default=timezone.now)
    data_recebimento = models.DateField("Data do recebimento", null=True, blank=True)

    def __str__(self):
        op_comprovacao = tipocomprovacao()
        nr_doc = "nº {}".format(self.nr_doc_comprovacao) if self.nr_doc_comprovacao else ""
        return "{} ".format([(forma) for forma in op_comprovacao if self.tipo_comprovacao in forma][0][1]) + nr_doc

    @property
    def meio_comprovacao(self):
        meios = tipocomprovacao()
        nome_meio = ""
        for meio in meios:
            if meio[0] == self.tipo_comprovacao:
                nome_meio = meio[1]
        return nome_meio