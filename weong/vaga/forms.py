import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Vaga
from usuario.forms import CadastroEnderecoForm
from .services import possui_candidatura

class VagaForm(forms.ModelForm):
    titulo = forms.CharField(max_length=100, label='Título da vaga')
    descricao = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length=5000, label='Descrição da vaga')
    requisitos = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length=2500, label='Requisitos da vaga')
    quantidade_vagas = forms.CharField(label='Quantidade de vagas', widget=forms.NumberInput(attrs={'class':'form-control', 'max': 100}))
    fim_candidaturas = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'requisitos', 'quantidade_vagas', 'fim_candidaturas']

class EditarVagaForm(forms.ModelForm):

    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'requisitos', 'quantidade_vagas', 'fim_candidaturas']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'max_length': 100}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'max_length': 5000}),
            'requisitos': forms.Textarea(attrs={'class': 'form-control', 'max_length': 5000}),
            'quantidade_vagas': forms.NumberInput(attrs={'class':'form-control', 'max': 100}),
            'fim_candidaturas': forms.DateInput(attrs={'type':'date', 'initial': datetime.date.today}),
        }
    
    def __init__(self, *args, **kwargs):
        id_vaga = kwargs.pop('id_vaga', None)
        super().__init__(*args, **kwargs)

        if possui_candidatura(id_vaga):
            self.fields['titulo'].disabled = True
            self.fields['descricao'].disabled = True
            self.fields['requisitos'].disabled = True
    
    def clean_fim_candidaturas(self):
        fim_candidaturas = self.cleaned_data['fim_candidaturas']
        if fim_candidaturas < datetime.date.today():
            raise ValidationError(_('Fim de candidaturas deve ser a partir de hoje.'), code='invalido')
        return fim_candidaturas