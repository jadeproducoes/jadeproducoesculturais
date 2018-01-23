from django import forms
from .models import Arquivo

class FormUploadArquivo(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ('descricao', 'arquivo_carga', 'tipo_arquivo', 'funcao_arquivo')