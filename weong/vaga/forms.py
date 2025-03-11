from django import forms

from .models import Vaga

class VagaForm(forms.ModelForm):
    titulo = forms.CharField(max_length=100, label='Título da vaga',widget=forms.TextInput(attrs={'class':'form-control'}))
    descricao = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length=5000, label='Descrição da vaga')
    requisitos = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length=2500, label='Requisitos da vaga')
    quantidade_vagas = forms.IntegerField(max_value=100, label='Quantidade de vagas')
    fim_candidaturas = forms.CharField(widget=forms.DateField, label='Encerramento das candidaturas')
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'requisitos', 'quantidade_vagas', 'fim_candidaturas']