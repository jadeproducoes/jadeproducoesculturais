from django.db import models

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


class Arquivo(models.Model):

    descricao = models.TextField("Descreva o arquivo", blank=False)
    arquivo_carga = models.FileField("Carregar arquivo")
    tipo_arquivo = models.ForeignKey(TipoArquivo, verbose_name="Tipo de arquivo", null=True)
    funcao_arquivo = models.ForeignKey(FuncaoArquivo, verbose_name="Função", null=True)
    data_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_uploaded"]
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

    def __str__(self):
        return self.arquivo_carga.name

