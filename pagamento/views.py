from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from pagamento.models import *
from projeto.models import Projeto
from orcamento.models import Orcamento, RubricaOrcamento
from .forms import *

# Create your views here.
def index(request):
    pass

def pagamentos(request, id_projeto):

    lista_pagamentos = False
    projeto = Projeto.objects.get(pk=id_projeto)
    valor_total_orcamento = Orcamento.objects.filter(projeto_associado=projeto, orcamento_escolhido=True)[0].valor_liquido
    pagamentos = Pagamento.objects.filter(id_projeto=projeto).order_by('-data_pagamento')
    valor_total_pagamentos = 0

    if pagamentos.count() > 0:
        for pagamento in pagamentos:
            valor_pagamento = ItemPagamento.objects.filter(id_pagamento=pagamento).aggregate(somatorio=Sum('valor_bruto_pagamento'))
            if valor_pagamento['somatorio']:
                valor_total_pagamentos += valor_pagamento['somatorio']

        lista_pagamentos = []
        for pagamento in pagamentos:
            # recupera os itens do padamento para apresentar um texto curto para cada uma na lista
            itens_pagamentos = ItemPagamento.objects.filter(id_pagamento=pagamento.id)
            qtde_itens = itens_pagamentos.count()
            conta_itens = 0
            lista_itens = ""
            valor_pagamento = 0

            if qtde_itens > 0:
                for item in itens_pagamentos:
                    lista_itens += (str(item.id_rubrica)[0:20])
                    conta_itens += 1
                    if conta_itens < qtde_itens:
                        lista_itens += "\n"
                    valor_pagamento += item.valor_bruto_pagamento
            linha_item = [pagamento.id, lista_itens, pagamento.id_pessoa, valor_pagamento,
                          pagamento.data_pagamento, pagamento.pendencias_pagamento]
            lista_pagamentos.append(linha_item)

    return render(request, 'pagamento/pagamentos.html', {'lista_pagamentos':lista_pagamentos,
                                                         'projeto':projeto,
                                                         'valor_total_orcamento':valor_total_orcamento,
                                                         'valor_total_pagamentos':valor_total_pagamentos,
                                                         'saldo': (valor_total_orcamento - valor_total_pagamentos),
                                                         'tabelaIRRF':tabela_ativa_IRRF()})

def pagamento(request, id_pagamento):
    pagamento = Pagamento.objects.get(pk=id_pagamento)
    rubricas_pagamento = ItemPagamento.objects.filter(id_pagamento=pagamento)
    valor_pagamento = ItemPagamento.objects.filter(id_pagamento=pagamento).aggregate(Sum('valor_bruto_pagamento'))['valor_bruto_pagamento__sum']
    formas_pagamento = FormaDePagamento.objects.filter(id_pagamento=pagamento)
    excesso = Decimal(pagamento.valor_liquido - pagamento.soma_fomas_pagamento)
    formas_comprovavao = FormaComprovacao.objects.filter(id_pagamento=pagamento)
    return render(request, 'pagamento/pagamento.html', {'pagamento':pagamento,
                                                        'valor_pagamento': valor_pagamento,
                                                        'rubricas_pagamento':rubricas_pagamento,
                                                        'formas_pagamento':formas_pagamento,
                                                        'formas_comprovavao':formas_comprovavao,
                                                        'excesso':excesso})

def novopagamento(request, id_projeto):
    if not tabela_ativa_IRRF():
        return redirect('pagamentos', id_projeto=id_projeto)
    projeto = Projeto.objects.get(id=id_projeto)
    orcamento_ativo = Orcamento.objects.filter(projeto_associado=projeto, orcamento_escolhido=True)
    pagamento = Pagamento.objects.create(id_projeto=projeto, id_orcamento=orcamento_ativo[0])
    return redirect('pagamento', id_pagamento=pagamento.id)

def eliminapagamento(request, id_pagamento):
    projeto = Pagamento.objects.get(pk=id_pagamento).id_projeto
    pagamento = Pagamento.objects.get(pk=id_pagamento)
    pagamento.delete()
    return redirect('pagamentos', id_projeto=projeto.pk)

def novarubricapagamento(request, id_pagamento):
    pass

def listarubricasprojeto(request, id_pagamento):
    pagamento = Pagamento.objects.get(pk=id_pagamento)
    itens_pagamento = list(ItemPagamento.objects.filter(id_pagamento=pagamento).values('id_rubrica'))
    rubricas_pagamento = []
    for item in itens_pagamento:
        rubricas_pagamento.append(item['id_rubrica'])
    projeto = Projeto.objects.get(pk=pagamento.id_projeto.pk)
    orcamento_ativo = Orcamento.objects.filter(projeto_associado=projeto, orcamento_escolhido=True)[0]
    rubricas_orcamento = RubricaOrcamento.objects.filter(orcamento_associado=orcamento_ativo)
    return render(request, 'pagamento/rubricas_pagamentos.html',
                                                        {'pagamento':pagamento,
                                                        'rubricas_pagamento':rubricas_pagamento,
                                                        'projeto':projeto,
                                                        'rubricas_orcamento':rubricas_orcamento})

def atualizarubricas(request, id_pagamento):
    if request.method == 'POST':
        id_rubricas_selecionadas = request.POST.getlist('id_rubrica')
        pagamento = Pagamento.objects.get(pk=id_pagamento)

        if len(id_rubricas_selecionadas) > 0:
            itens_cadastrados = ItemPagamento.objects.filter(id_pagamento=pagamento)

            # 1a etapa - verifica se as rugbricas existentes no BD estao na lista de selecao das rubricas
            for item in itens_cadastrados:
                if not str(item.id_rubrica.pk) in id_rubricas_selecionadas:
                    item.delete()

            # 2a etapa - verifica se os itens selecionadso existem na tabela
            itens_cadastrados = ItemPagamento.objects.filter(id_pagamento=pagamento)

            for id_rubrica in id_rubricas_selecionadas:
                rubrica = RubricaOrcamento.objects.get(pk=id_rubrica)
                if not itens_cadastrados.filter(id_rubrica=rubrica).exists():
                    ItemPagamento.objects.create(id_pagamento=pagamento, id_rubrica=rubrica)

            #pagamento = Pagamento.objects.get(pk=id_pagamento)
            #for id_rubrica in id_rubricas_selecionadas:
            #    rubrica = RubricaOrcamento.objects.get(pk=id_rubrica)
            #    print("Rubrica inserida: " + str(id_rubrica))
            #    ItemPagamento.objects.create(id_pagamento=pagamento, id_rubrica=rubrica)
        else:
            ItemPagamento.objects.filter(id_pagamento=id_pagamento).delete()

    return redirect('pagamento', id_pagamento=id_pagamento)

def novaformapagamento(request, id_pagamento):
    forma_pagamento = FormaDePagamento.objects.create(id_pagamento=Pagamento.objects.get(pk=id_pagamento))
    formulario = FormularioFormaPagamento(instance=forma_pagamento)
    return render(request, 'pagamento/editaformapagamento.html', {'formulario': formulario,
                                                                  'id_forma_pagamento': forma_pagamento.pk})

def editaformapagamento(request, id_forma_pagamento):
    forma_pagamento = FormaDePagamento.objects.get(pk=id_forma_pagamento)
    if request.method == 'POST':
        formulario = FormularioFormaPagamento(request.POST, instance=forma_pagamento)
        if formulario.is_valid():
            formulario.save()
            return redirect('pagamento', id_pagamento=forma_pagamento.id_pagamento.pk)
    else:
        formulario = FormularioFormaPagamento(instance=forma_pagamento)

    return render(request, 'pagamento/editaformapagamento.html', {'formulario': formulario,
                                                                  'id_forma_pagamento': id_forma_pagamento})

def eliminaformapagamento(request, id_forma_pagamento):
    elimina_forma_pagamento = FormaDePagamento.objects.get(pk=id_forma_pagamento)
    id_pagamento = elimina_forma_pagamento.id_pagamento.pk
    elimina_forma_pagamento.delete()
    return redirect('pagamento', id_pagamento=id_pagamento)

def novaformacomprovacao(request, id_pagamento):
    forma_comprovacao = FormaComprovacao.objects.create(id_pagamento=Pagamento.objects.get(pk=id_pagamento))
    formulario = FormularioFormaComprovacao(instance=forma_comprovacao)
    return render(request, 'pagamento/editaformacomprovacao.html', {'formulario':formulario,
                                                                    'id_forma_comprovacao':forma_comprovacao.pk})
def editaformacomprovacao(request, id_forma_comprovacao):
    forma_comprovacao = FormaComprovacao.objects.get(pk=id_forma_comprovacao)
    if request.method == 'POST':
        formulario = FormularioFormaComprovacao(request.POST, instance=forma_comprovacao)
        if formulario.is_valid():
            formulario.save()
            return redirect('pagamento', id_pagamento=forma_comprovacao.id_pagamento.pk)
    else:
        formulario = FormularioFormaComprovacao(instance=forma_comprovacao)

    return render(request, 'pagamento/editaformacomprovacao.html', {'formulario': formulario,
                                                                  'id_forma_comprovacao': id_forma_comprovacao})
def eliminaformacomprovacao(request, id_forma_comprovacao):
    elimina_forma_comprovacao = FormaComprovacao.objects.get(pk=id_forma_comprovacao)
    id_pagamento = elimina_forma_comprovacao.id_pagamento.pk
    elimina_forma_comprovacao.delete()
    return redirect('pagamento', id_pagamento=id_pagamento)

def eliminaitempagamento(request, id_item):
    elimina_rubrica = ItemPagamento.objects.get(pk=id_item)
    id_pagamento = elimina_rubrica.id_pagamento.pk
    elimina_rubrica.delete()
    return redirect('pagamento', id_pagamento=id_pagamento)

def editaitempagamento(request, id_item):
    edita_rubrica = ItemPagamento.objects.get(pk=id_item)
    if request.method == 'POST':
        formulario = FormularioItemPagamento(request.POST,instance=edita_rubrica)
        if formulario.is_valid():
            formulario.save()
            return redirect('pagamento', id_pagamento=edita_rubrica.id_pagamento.pk)
    else:
        formulario = FormularioItemPagamento(instance=edita_rubrica)

    return render(request, 'pagamento/editaitempagamento.html', {'formulario':formulario, 'id_item':id_item})


def editadescontos(request, id_pagamento):
    pagamento = Pagamento.objects.get(pk=id_pagamento)
    if request.method == 'POST':
        formulario = FormularioDescontos(request.POST, instance=pagamento)
        if formulario.is_valid():
            formulario.save()
            return redirect('pagamento', id_pagamento=id_pagamento)
    else:
        formulario = FormularioDescontos(instance=pagamento)
    return render(request, 'pagamento/editadescontos.html', {'formulario':formulario, 'id_pagamento':id_pagamento})

def cancelardescontos(request, id_pagamento):
    pagamento = Pagamento.objects.get(pk=id_pagamento)
    pagamento.cobrar_ISS = False
    pagamento.cobrar_INSS = False
    pagamento.save()
    return redirect('pagamento', id_pagamento=id_pagamento)

def alterarbenefiario(request, id_pagamento):
    pagamento = Pagamento.objects.get(pk=id_pagamento)
    if request.method == 'POST':
        formulario = FormularioBeneficiario(request.POST, instance=pagamento)
        if formulario.is_valid():
            formulario.save()
            return redirect('pagamento', id_pagamento=id_pagamento)
    else:
        formulario = FormularioBeneficiario(instance=pagamento)
    return render(request, 'pagamento/beneficiariopagamento.html', {'formulario':formulario, 'id_pagamento':id_pagamento})


