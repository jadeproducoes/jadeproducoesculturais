from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Projeto, Tarefa
from utils.utilitarios import *
from openpyxl import Workbook
from openpyxl import load_workbook
import datetime
from carregaarquivo.views import Carregaarquivo

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
    print("Entrei nada!" + str(tarefas))
    if tarefas:
        cor_prioridade = ""
        print("Pelo menos entrei")
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
            print(item)
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



'''
    if request.method == 'POST' and request.FILES['planilha']:
        planilha = request.FILES['planilha']
        fs = FileSystemStorage()
        filename = fs.save(planilha.name, planilha)
        uploadad_file_url = fs.url(filename)
        return render(request, 'projeto/carregaorcamento.html', {'uploadad_file_url':uploadad_file_url})
'''