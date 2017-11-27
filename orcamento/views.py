from django.http import HttpResponse
from django.shortcuts import render
from projeto.models import *
from .models import *

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def ultimoorcamento(request):
    try:
        ultimo_orcamento = Orcamento.objects.latest('data_criacao_orcamento') # não é esse dado. consertar isso
    except Orcamento.DoesNotExist:
        raise Http404("Não existe nenhum orçamento cadastrado")

    try:
        lista_rubricas = RubricaOrcamento.objects.filter(orcamento_associado=ultimo_orcamento.id).order_by('numero_rubrica')
    except RubricaOrcamento.DoesNotExist:
        raise Http404("Não existm rubricas cadastradas para o último orçamento")


    return render(request,'orcamento/orcamento.html', {'lista_rubricas': lista_rubricas})
