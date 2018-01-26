from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from projeto.models import Projeto
from django import forms
from .models import *
from .forms import *
from projeto.forms import FormListaProjetos
from pagamento.models import Pagamento, ItemPagamento
from utils.utilitarios import *
from openpyxl import load_workbook
from carregaarquivo.models import Arquivo, TipoArquivo, FuncaoArquivo
from carregaarquivo.views import Carregaarquivo, ImportaPlanilha, FiltroImportacao
from carregaarquivo.forms import FormExibePlanilha
import xlrd


def index(request):
    lista_projetos = Projeto.objects.all()
    return render(request, 'orcamento/orcamento.html', {'lista_projetos':lista_projetos,
                                                        'titulo_pagina':'Orçamento',})

def listaorcamentos(request, id):
    projeto = Projeto.objects.get(id=id)
    lista_orcamentos = Orcamento.objects.filter(projeto_associado=projeto)
    return render(request, 'orcamento/listaorcamentos.html', {'projeto': projeto,
                                                              'lista_orcamentos':lista_orcamentos,
                                                              'titulo_pagina':'Lista orçamentos',})

def total_bruto(lista_rubricas):
    total_bruto = 0
    for rubrica in lista_rubricas:
        total_bruto += (rubrica.valor_solicitado * rubrica.quantidade)
    return total_bruto


def total_glosas(lista_rubricas):
    total_glosas = 0
    for rubrica in lista_rubricas:
        total_glosas += (rubrica.valor_da_glosa * rubrica.quantidade)
    return total_glosas

def total_liquido(lista_rubricas):
    return total_bruto(lista_rubricas)-total_glosas(lista_rubricas)

def ordena_rubricas(rubricas):
    cont = 1
    for rubrica in rubricas:
        rubrica.numero_rubrica = cont
        rubrica.save()
        cont += 1

def exibeorcamento(request, id):
    orcamento = Orcamento.objects.get(pk=id)
    rubricas = orcamento.rubricas_orcamento
    # coloca um numero de ordem nas rubricas
    if rubricas.filter(numero_rubrica=0).exists():
        ordena_rubricas(rubricas)
    # elimina brechas provenientes de delecao de objetos
    rubricas = rubricas.order_by('numero_rubrica')
    ordena_rubricas(rubricas)
    return render(request, 'orcamento/exibeorcamento.html', {'titulo_pagina':'Exibe orçamento', 'orcamento':orcamento})

'''   
    identifica_orcamento = orcamento.descricao_orcamento
    projeto_associado = orcamento.projeto_associado
    lista_rubricas = RubricaOrcamento.objects.filter(orcamento_associado=id).order_by('id')
    qtde_itens = lista_rubricas.count()
    if qtde_itens>0:
        # APENAS PARA TESTE - RESSETAR O MODELO
        #orcamento.rubricas_ordenadas = False
        if not orcamento.rubricas_ordenadas:
            cont = 1
            for rubrica in lista_rubricas:
                print(rubrica)
                rubrica.numero_rubrica = cont
                rubrica.save()
                cont += 1
            orcamento.rubricas_ordenadas=True
            orcamento.save()
        else:
            novas_rubricas = lista_rubricas.filter(numero_rubrica=0).order_by('-id')
            qtde_novas_rubricas = novas_rubricas.count()
            if qtde_novas_rubricas>0:
                rubricas_antigas = lista_rubricas.exclude(numero_rubrica=0)
                for rubrica_antiga in rubricas_antigas:
                    rubrica_antiga.numero_rubrica += qtde_novas_rubricas
                    rubrica_antiga.save()
                cont = 1
                for nova_rubrica in novas_rubricas:
                    nova_rubrica.numero_rubrica = cont
                    nova_rubrica.save()
                    cont+=1
            else:

    # segunda passagem para evitar brechas na lista proveniente de exclusoes de registros
    lista_rubricas = lista_rubricas.order_by('numero_rubrica')
    cont = 1
    for rubrica in lista_rubricas:
        rubrica.numero_rubrica = cont
        rubrica.save()
        cont+=1
    nr_itens = lista_rubricas.count()

    
 
    Deixei esse trecho para avaliar a evolucao no conceito do Django
    return render(request, 'orcamento/exibeorcamento.html', {'nome_projeto':projeto_associado,
                                                             'id_projeto':orcamento.projeto_associado.id,
                                                             'id_orcamento': id,
                                                             'orcamento_ativo':orcamento.orcamento_escolhido,
                                                             'identifica_orcamento':identifica_orcamento,
                                                             'nr_itens':nr_itens,
                                                             'lista_rubricas':lista_rubricas,
                                                             'total_bruto':total_bruto(lista_rubricas),
                                                             'total_glosas':total_glosas(lista_rubricas),
                                                             'total_liquido':total_liquido(lista_rubricas),
                                                             'titulo_pagina':'Exibe orçamento',
                                                             'orcamento':orcamento})
'''

def ultimoorcamento(request):
    ultimo_orcamento = Orcamento.objects.latest('data_criacao_orcamento') # não é esse dado. consertar isso
    return redirect('exibeorcamento', id=ultimo_orcamento.id)

def primeirarubricadalista(request, id):
    rubrica = RubricaOrcamento.objects.get(id=id)
    rubrica.numero_rubrica = 0
    rubrica.save()
    return redirect('exibeorcamento', id=rubrica.orcamento_associado.id)

def ultimarubricadalista(request, id):
    rubrica = RubricaOrcamento.objects.get(id=id)
    qtde_itens = RubricaOrcamento.objects.filter(orcamento_associado=rubrica.orcamento_associado.id).count()
    rubrica.numero_rubrica = qtde_itens + 1
    rubrica.save()
    return redirect('exibeorcamento', id=rubrica.orcamento_associado.id)

def umarubricacima(request, id):
    rubrica = RubricaOrcamento.objects.get(id=id)
    posicao_atual = rubrica.numero_rubrica
    posicao_final = posicao_atual - 1
    rubricas = RubricaOrcamento.objects.filter(orcamento_associado=rubrica.orcamento_associado.id)
    rubrica_anterior = rubricas.get(numero_rubrica=posicao_final)
    rubrica_anterior.numero_rubrica = posicao_atual
    rubrica_anterior.save()
    rubrica.numero_rubrica = posicao_final
    rubrica.save()
    return redirect('exibeorcamento', id=rubrica.orcamento_associado.id)

def umarubricabaixo(request, id):
    rubrica = RubricaOrcamento.objects.get(id=id)
    posicao_atual = rubrica.numero_rubrica
    posicao_final = posicao_atual + 1
    rubricas = RubricaOrcamento.objects.filter(orcamento_associado=rubrica.orcamento_associado.id)
    rubrica_anterior = rubricas.get(numero_rubrica=posicao_final)
    rubrica_anterior.numero_rubrica = posicao_atual
    rubrica_anterior.save()
    rubrica.numero_rubrica = posicao_final
    rubrica.save()
    return redirect('exibeorcamento', id=rubrica.orcamento_associado.id)

def novarubrica(request, id):
    if request.method == 'POST':
        formulario = FormularioRubricas(request.POST)
        if formulario.is_valid():
            rubrica = formulario.save(commit=False)
            rubrica.orcamento_associado = Orcamento.objects.get(pk=id)
            salvo = rubrica.save()
            print("Retorno de salvo: " + str(salvo))
            return redirect('exibeorcamento', id=id)
    else:
        formulario = FormularioRubricas()

    return render(request, 'orcamento/novarubrica.html', {'formulario':formulario, 'id':id})

def editarubrica(request, id):
    rubrica = get_object_or_404(RubricaOrcamento, id=id)
    if request.method == 'POST':
        formulario = FormularioRubricas(request.POST, instance=rubrica)
        if formulario.is_valid():
            formulario.save()
            return redirect('exibeorcamento', id=rubrica.orcamento_associado.id)
    else:
        formulario = FormularioRubricas(instance=rubrica)

    return render(request, 'orcamento/editarubrica.html', {'formulario':formulario, 'id':id})

def exiberubrica(request, id, id_orcamento):
    rubrica = RubricaOrcamento.objects.get(id=id)
    orcamento = rubrica.orcamento_associado
    projeto = rubrica.orcamento_associado.projeto_associado

    return render(request, 'orcamento/exiberubrica.html', {'id':id,
                                                           'id_orcamento':id_orcamento,
                                                           'rubrica': rubrica,
                                                           'orcamento':orcamento,
                                                           'projeto':projeto})

def eliminarubrica(request, id, id_orcamento):
    '''
    View que elimina uma determinada rubrica.

    :param request:
    :param id: id da rubrica a ser eliminada
    :param id_orcamento: id do orcamento a que esta associada a rubrica
    :return: id do orcamento
    '''
    rubrica = RubricaOrcamento.objects.get(id=id)
    rubrica.delete()
    return redirect('exibeorcamento', id=id_orcamento)

def ativarorcamento(request, id):
    '''
    View que permite indicar que o orcamento atual e o orcamento do proejto (orcamento ativo)

    :param request:
    :param id: id do orcamento atual
    :return: id do orcamento atual
    '''
    orcamento_atual = Orcamento.objects.get(id=id)
    # a partir do projeto atual do orcamento, filtra os demais orcamentos relacionados ao mesmo projeto
    todos_orcs_mesmo_projeto = Orcamento.objects.filter(projeto_associado=orcamento_atual.projeto_associado)
    todos_orcs_mesmo_projeto.update(orcamento_escolhido=False)
    orcamento_atual.orcamento_escolhido = True
    orcamento_atual.save()
    return redirect('exibeorcamento', id=id)

def desativarorcamento(request, id):
    '''
    View que permite desmarcar um orcamento como o orcamento ativo de um projeto.

    :param request:
    :param id: identificacao do orcamento atual
    :return: id do orcamento atual
    '''
    orcamento_atual = Orcamento.objects.get(id=id)
    orcamento_atual.orcamento_escolhido = False
    orcamento_atual.save()
    return redirect('exibeorcamento', id=id)

def controleorcamentario(request, id_projeto):
    '''
    View que recupera as informacoes para exibicao dos dados de controle orcamentario.

    :param request:
    :param id_projeto:
    :return:
    '''
    orcamento = orcamento_ativo(id_projeto) # Isso nao resolve o problema das mudancas orcamentarias
    rubricas = RubricaOrcamento.objects.filter(orcamento_associado=orcamento)
    pagamentos = Pagamento.objects.filter(id_orcamento=orcamento)

    linha = {}
    orcamento_controlado = []
    total_usado = 0
    total_saldo = 0

    for rubrica in rubricas:
        valor_usado = 0
        for pagamento in pagamentos:
            if ItemPagamento.objects.filter(id_pagamento=pagamento).exists():
                itens_pagamento = ItemPagamento.objects.filter(id_pagamento=pagamento)
                for item in itens_pagamento:
                    if item.id_rubrica == rubrica:
                        valor_usado += item.valor_bruto_pagamento

        valor_liquido_rubrica = (rubrica.valor_solicitado - rubrica.valor_da_glosa) * rubrica.quantidade
        saldo =  valor_liquido_rubrica - valor_usado
        total_usado += valor_usado
        total_saldo += saldo
        linha['rubrica'] = rubrica
        linha['utilizado'] = valor_usado
        linha['saldo'] = saldo
        linha['percentual_usado'] = (valor_usado / valor_liquido_rubrica) * 100
        linha['percentual_saldo'] = (saldo / valor_liquido_rubrica) * 100

        if linha['percentual_usado'] <= 50:
            linha['cor'] = cores('padrao')
        elif linha['percentual_usado'] > 50 and linha['percentual_usado'] <= 90:
            linha['cor'] = cores('alerta')
        else:
            linha['cor'] = cores('critico')

        orcamento_controlado.append((linha))
        linha = {}

    return render(request, 'orcamento/controleorcamentario.html', {'orcamento':orcamento_controlado,
                                                                   'orcamento_base':orcamento,
                                                                   'total_usado':total_usado,
                                                                   'total_saldo':total_saldo,
                                                                   'titulo_pagina':'Controle Orçamentário'})

def download_controle_excel(request, id_projeto):
    pass

def novoorcamento(response, id_projeto):
    pass

def baixa_planilha_excel(response):
    pass

def carrega_orcamento(request):
    '''
    View que constroi o formulario de upload das planilhas.

    :param request:
    :return: objeto upload_engine contendo formulario para upload de planilhas
    '''
    upload_engine = Carregaarquivo()
    if not upload_engine.model_form_upload(request):
        return redirect('planilhascarregadas')
    return render(request, 'orcamento/carregaorcamento.html', {'upload':upload_engine})

def planilhascarregadas(request):
    '''
    Recupera a lista das planilhas que foram carregadas para a pasta MEDIA.
    :param request:
    :return: lista dos registros contendo os arquivos de planilha
    '''
    arquivos_planilha = TipoArquivo.objects.filter(extencao_arquivo__in = ['xls', 'xlsx'])
    funcao_orcamento = FuncaoArquivo.objects.filter(sigla_funcao='PLO')
    arquivos = Arquivo.objects.filter(tipo_arquivo__in = list(arquivos_planilha), funcao_arquivo = funcao_orcamento[0])
    return render(request, 'orcamento/lista_planilhas_carregadas.html', {'arquivos':arquivos})

def exibir_planilha(request, id_arquivo):
    '''
    Monta e exibe uma tabela a partir de uma planilha excel carregada previamente carregada na pasta MEDIA.

    :param request: class HttpRequest
    :param id_arquivo: PK proveniente da tabela de dados dos arquivos carregados na pasta MEDIA
    :return: uma STR contendo a tabela a ser renderizada no template
    '''
    planilha = ""
    arquivo = Arquivo.objects.get(pk=id_arquivo)

    if arquivo:

        linha_inicial = 1
        linha_final = 20
        coluna_inicial = 'A'
        coluna_final = 'J'

        if request.method == 'POST':
            formulario = FormExibePlanilha(request.POST)
            if formulario.is_valid():
                linha_inicial = int(formulario.cleaned_data['linha_inicial'])
                linha_final = int(formulario.cleaned_data['linha_final'])
                coluna_inicial = formulario.cleaned_data['coluna_inicial']
                coluna_final = formulario.cleaned_data['coluna_final']
        else:
            dados = {'linha_inicial': linha_inicial,
                     'linha_final': linha_final,
                     'coluna_inicial': coluna_inicial,
                     'coluna_final': coluna_final}
            formulario = FormExibePlanilha(dados)

        ipp = ImportaPlanilha()
        ipp.linha_inicial = linha_inicial
        ipp.linha_final = linha_final
        ipp.coluna_final = coluna_inicial
        ipp.coluna_final = coluna_final
        planilha_importada = ipp.importa_planilha(arquivo)

        tb = TabelaHTML()
        tb.class_padrao = 'table table-bordered'
        if planilha_importada:
            tb.numera_linhas = True
            planilha = tb.gerar_tabela(planilha_importada)
        else:
            tb.numera_linhas = False
            planilha = 'Não foi possível importar a planilha. Verifique se o filtro está ajustado ou se o arquivo está presente'

    return render(request, 'orcamento/exibe_planilha.html', {'planilha':planilha, 'arquivo':arquivo, 'formulario':formulario})

