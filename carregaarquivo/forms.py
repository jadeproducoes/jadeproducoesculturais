from django import forms
from .models import Arquivo, TipoArquivo
from projeto.models import Projeto

class FormUploadArquivo(forms.ModelForm):

    #def clean_objeto_associado(self):
    #    objeto_associado = self.cleaned_data['objeto_associado']
    #    print("***** Objeto: {} Escondidos: {}".format(objeto_associado, self.hidden_fields()))
    #    return objeto_associado
    class Meta:
        model = Arquivo
        fields = ('descricao', 'arquivo_carga', 'tipo_arquivo', 'funcao_arquivo', 'filtro', 'objeto_associado')
        widgets = {'objeto_associado': forms.HiddenInput()}

class FormExibePlanilha(forms.Form):
    linha_final = forms.CharField(widget=forms.NumberInput(attrs={'size':'3', 'max_length':'3'}), label="Nova linha final")
    desconsiderar_linhas = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':'50', 'max_length':'50'}),
                                           help_text='Ex.: 5-9;14;34-40 (desconsidera as linhas 5 a 9, 14 e de 34 a 40)')
    VISUALIZA = [('Visualizar', 'Visualizar'), ('Importar', 'Importar')]
    acao = forms.ChoiceField(choices=VISUALIZA, widget=forms.RadioSelect(), initial='Vizualizar', required=False)
    #linha_inicial = forms.CharField(widget=forms.NumberInput(attrs={'size':'3', 'max_length':'3'}))
    #coluna_inicial = forms.CharField(widget=forms.TextInput(attrs={'size':'2', 'max_length':'2'}))
    #coluna_final = forms.CharField(widget=forms.TextInput(attrs={'size':'3','max_length':'2'}))
    #desconsiderar_colunas = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':'50', 'max_length':'50'}))

