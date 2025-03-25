import datetime
from django import forms

from .models import Vaga
from usuario.forms import CadastroEnderecoForm

class VagaForm(forms.ModelForm):
    titulo = forms.CharField(max_length=100, label='Título da vaga')
    descricao = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length=5000, label='Descrição da vaga')
    requisitos = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length=2500, label='Requisitos da vaga')
    quantidade_vagas = forms.CharField(label='Quantidade de vagas', widget=forms.NumberInput(attrs={'class':'form-control', 'max': 100}))
    fim_candidaturas = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'requisitos', 'quantidade_vagas', 'fim_candidaturas']