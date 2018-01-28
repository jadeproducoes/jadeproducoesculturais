from django import forms
from .models import Arquivo

class FormUploadArquivo(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ('descricao', 'arquivo_carga', 'tipo_arquivo', 'funcao_arquivo')

class FormExibePlanilha(forms.Form):
    linha_final = forms.CharField(widget=forms.NumberInput(attrs={'size':'3', 'max_length':'3'}), label="Nova linha final")
    desconsiderar_linhas = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':'50', 'max_length':'50'}))
    VISUALIZA = [('Visualizar', 'Visualizar'), ('Importar', 'Importar')]
    acao = forms.ChoiceField(choices=VISUALIZA, widget=forms.RadioSelect(), initial=[('Visualizar', 'Visualizar')])
    #linha_inicial = forms.CharField(widget=forms.NumberInput(attrs={'size':'3', 'max_length':'3'}))
    #coluna_inicial = forms.CharField(widget=forms.TextInput(attrs={'size':'2', 'max_length':'2'}))
    #coluna_final = forms.CharField(widget=forms.TextInput(attrs={'size':'3','max_length':'2'}))
    #desconsiderar_colunas = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':'50', 'max_length':'50'}))

