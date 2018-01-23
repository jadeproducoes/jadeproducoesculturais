from django import forms
from .models import *

class FormularioRubricas(forms.ModelForm):
    class Meta:
        model = RubricaOrcamento
        fields = '__all__'
        exclude = ['orcamento_associado', 'numero_rubrica']
