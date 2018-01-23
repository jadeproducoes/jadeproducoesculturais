from django import forms
from .models import Projeto

class FormListaProjetos(forms.Form):
    projeto_ativo = 0
    id_projeto = forms.ModelMultipleChoiceField(queryset=Projeto.objects.all().order_by('-id'),
                                                widget=forms.Select(),
                                                initial=projeto_ativo,
                                                label='Projeto')
