from django import forms

from .models import Vaga

class VagaForm(forms.ModelForm):
    titulo = forms.CharField(max_length=100, label='Título da vaga')
    descricao = forms.CharField(widget=forms.Textarea, max_length=5000, label='Descrição da vaga')
    requisitos = forms.CharField(widget=forms.Textarea, max_length=2500, label='Requisitos da vaga')
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'requisitos']