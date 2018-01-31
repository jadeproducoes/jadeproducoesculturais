from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from carregaarquivo.forms import FormExibePlanilha
from carregaarquivo.models import Arquivo, FuncaoArquivo, TipoArquivo
from .models import Projeto, Tarefa
from utils.utilitarios import *
from openpyxl import Workbook
from openpyxl import load_workbook
import datetime
from carregaarquivo.views import Carregaarquivo, ImportaPlanilha


# Create your views here.

def index(request):
    projetos = Projeto.objects.all()
    return render(request, 'projeto/listaprojetos.html', {'projetos':projetos,})

def tarefas(request, id_projeto):
    projeto = Projeto.objects.get(pk=id_projeto)
    tarefas = Tarefa.objects.filter(projeto=projeto).order_by('status','prioridade','data_criacao')
    pendentes = {}
    em_andamento = {}
    concluidas = {}
    if tarefas:
        cor_prioridade = ""
        for tarefa in tarefas:
            envolvidos = "Responsável: " + str(tarefa.responsavel) + "\nEnvolvidos: " + tarefa.envolvidos
            if tarefa.prioridade == 0:
                cor_prioridade = cores('critica')
            elif tarefa.prioridade == 1:
                cor_prioridade = cores('alerta')
            else:
                cor_prioridade = cores('padrao')
            item = {'descricao': tarefa.desricao_tarefa,
                    'envolvidos':envolvidos,
                    'meta':tarefa.meta,
                    'prioridade':tarefa.prioridade,
                    'data_criacao':tarefa.data_criacao,
                    'data_limite':tarefa.data_conclusao,
                    'cor_prioridade':cor_prioridade}
            if tarefa.status == 0:
                pendentes[tarefa.pk] = item
            elif tarefa.status == 1:
                em_andamento[tarefa.pk] = item
            else:
                concluidas[tarefa.pk] = item

    return render(request, 'projeto/exibe_tarefas.html', {'projeto':projeto,
                                                          'pendentes':pendentes,
                                                          'em_andamento':em_andamento,
                                                          'concluidas':concluidas})

def editatarefa(request, id_tarefa):
    pass

def tarefaemandamento(request, id_tarefa):
    pass

def tarefaconcluida(request, id_tarefa):
    pass

def tarefapendente(request, id_tarefa):
    pass

def carrega_orcamento(request, id_projeto):
    '''
    View que constroi o formulario de upload das planilhas.

    :param request:
    :return: objeto upload_engine contendo formulario para upload de planilhas
    '''
    upload_engine = Carregaarquivo()
    upload_engine.objeto_associado = 'Projeto.pk=[{}]'.format(id_projeto)
    if not upload_engine.model_form_upload(request):
        return redirect('planilhascarregadas', id_projeto=id_projeto)
    return render(request, 'projeto/carregaorcamento.html', {'upload':upload_engine})

def planilhascarregadas(request, id_projeto):
    '''
    Recupera a lista das planilhas que foram carregadas para a pasta MEDIA.
    :param request:
    :return: lista dos registros contendo os arquivos de planilha
    '''
    projeto = Projeto.objects.get(pk=id_projeto)
    arquivos_planilha = TipoArquivo.objects.filter(extencao_arquivo__in = ['xls', 'xlsx'])
    funcao_orcamento = FuncaoArquivo.objects.filter(sigla_funcao='PLO')
    arquivos = Arquivo.objects.filter(tipo_arquivo__in = list(arquivos_planilha),
                                      funcao_arquivo = funcao_orcamento[0],
                                      objeto_associado__contains = 'Projeto.pk=[{}]'.format(id_projeto))
    return render(request, 'projeto/lista_planilhas_carregadas.html', {'arquivos':arquivos, 'projeto':projeto})

def exibir_planilha(request, id_projeto, id_arquivo):
    '''
    Monta e exibe uma tabela a partir de uma planilha excel carregada previamente carregada na pasta MEDIA.

    :param request: class HttpRequest
    :param id_arquivo: PK proveniente da tabela de dados dos arquivos carregados na pasta MEDIA
    :return: uma STR contendo a tabela a ser renderizada no template
    '''

    projeto = Projeto.objects.get(pk=id_projeto)
    planilha = ""
    arquivo = Arquivo.objects.get(pk=id_arquivo)

    if arquivo:

        planilha_importada = False
        desconsiderar_linha = ""

        ipp = ImportaPlanilha()
        if arquivo.filtro:
            ipp.ativa_filtro(arquivo.filtro)

        if request.method == 'POST':
            formulario = FormExibePlanilha(request.POST, initial={'acao': 'Vizualizar'})
            if formulario.is_valid():
                ipp.set_linha_final(int(formulario.cleaned_data['linha_final']))
                desconsiderar_linha = formulario.cleaned_data['desconsiderar_linhas']
                ipp.set_desconsidera_linhas(desconsiderar_linha)
                if formulario.cleaned_data['acao'] == 'Importar':
                    print("*****Agora vou importar com a porra toda*****")
        else:
            if arquivo.filtro:
                desconsiderar_linha = arquivo.filtro.excecao_linhas
                formulario = FormExibePlanilha({'linha_final':arquivo.filtro.linha_final,
                                                'desconsiderar_linhas':desconsiderar_linha},
                                               initial={'acao': 'Vizualizar'})
            else:
                formulario = FormExibePlanilha(initial={'acao': 'Vizualizar'})

        planilha_importada = ipp.importa_planilha(arquivo)

        tb = TabelaHTML()
        tb.class_padrao = 'table table-bordered'
        if planilha_importada:
            tb.numera_linhas = True
            tb.inicio_contagem = ipp.get_linha_inicial()
            tb.intevalo_marcacao_cor_especial = lista_de_intervalos(desconsiderar_linha)
            tb.cor_especial = cores('alerta')
            planilha = tb.gerar_tabela(planilha_importada)
        else:
            tb.numera_linhas = False
            planilha = 'Não foi possível importar a planilha. Verifique se o filtro está ajustado ou se o arquivo está presente'

    return render(request, 'projeto/exibe_planilha.html', {'planilha':planilha,'arquivo':arquivo,
                                                           'formulario':formulario, 'projeto':projeto})

