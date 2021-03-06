from enum import Enum

from django.db import models
from django import forms
from projeto.models import Projeto
import collections

# Create your models here.

class TipoArquivo(models.Model):

    descricao_tipo_arquivo = models.CharField("Descrição do tipo de arquivo", max_length=75, blank=False)
    extencao_arquivo = models.CharField("Extenção do tipo de arquivo", max_length=4, blank=False)

    class Meta:
        ordering = ["descricao_tipo_arquivo"]
        verbose_name = "Tipo de Arquivo"
        verbose_name_plural = "Tipos de Arquivos"

    def __str__(self):
        return self.descricao_tipo_arquivo

class FuncaoArquivo(models.Model):

    descricao_funcao_arquivo = models.CharField("Função do arquivo", max_length=50, blank=False)
    sigla_funcao = models.CharField("Sigla função", max_length=3, blank=False, default="")

    class Meta:
        ordering = ["descricao_funcao_arquivo"]
        verbose_name = "Função do Arquivo"
        verbose_name_plural = "Funções dos Arquivos"

    def __str__(self):
        return self.descricao_funcao_arquivo

class ModeloAlvo(models.Model):
    nome_modelo = models.CharField("Nome do modelo alvo", max_length=25, blank=False)
    app_modelo = models.CharField("Aplicativo do modelo", max_length=50, blank=False)

    class Meta:
        ordering = ["nome_modelo"]
        verbose_name = "Modelo alvo"
        verbose_name_plural = "Modelos alvos"

    def __str__(self):
        return self.nome_modelo

class FiltroImportacao(models.Model):

    nome_filtro = models.CharField("Nome do filtro", max_length=40, blank=False)
    descricao_filtro = models.TextField("Descrição da função do filtro", blank=True)
    modelo_destino = models.ForeignKey(ModeloAlvo, verbose_name="Nome da tabela de destino", on_delete=models.SET_NULL, null=True)
    correspondencias_campos = models.TextField("Correspondência entre campos e colunas planilha", blank=True)
    tipo_arquivo = models.ForeignKey(TipoArquivo, verbose_name="Se aplica a que tipo de arquivo?", on_delete=models.SET_NULL, null=True)
    linha_inicial = models.PositiveIntegerField("Linha inicial", default=0)
    linha_final = models.PositiveIntegerField("Linha final", default=20)
    coluna_inicial = models.CharField("Coluna inicial", max_length=3, default='A')
    coluna_final = models.CharField("Coluna final", max_length=3, default='L')
    excecao_linhas = models.CharField("Linhas que não devem ser processadas", max_length=50, blank=True)
    excecao_colunas = models.CharField("Colunas que não devem ser processadas", max_length=50, blank=True)
    funcoes_colunas = models.TextField("Quais as funções que serão aplicadas as colunas", blank=True)
    funcoes_linhas = models.TextField("Quais as funções que serão aplicadas as linhas", blank=True)

    @property
    def parametros(self):
        return "Linha inicial: {} Linha final: {} Coluna inicial: {} Coluna final: {}".\
            format(self.linha_inicial, self.linha_final, self.coluna_inicial, self.coluna_final)

    def __str__(self):
        return self.nome_filtro

    class Meta:
        ordering = ["nome_filtro"]
        verbose_name = "Filtro de importação"
        verbose_name_plural = "Filtro de importações"

class Arquivo(models.Model):
    descricao = models.TextField("Descreva o arquivo", blank=False)
    arquivo_carga = models.FileField("Carregar arquivo")
    tipo_arquivo = models.ForeignKey(TipoArquivo, verbose_name="Tipo de arquivo", null=True, on_delete=models.SET_NULL)
    funcao_arquivo = models.ForeignKey(FuncaoArquivo, verbose_name="Função", null=True, on_delete=models.SET_NULL)
    filtro = models.ForeignKey(FiltroImportacao, verbose_name="Filtro de importação", null=True, on_delete=models.SET_NULL)
    objeto_associado = models.CharField(blank=True, default='0', max_length=60)
    data_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_uploaded"]
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

    def __str__(self):
        return self.arquivo_carga.name


