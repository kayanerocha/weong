import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Vaga
from usuario.forms import CadastroEnderecoForm, EditarEnderecoForm
from .services import qnt_candidatos_selecionados, possui_candidatura

class VagaForm(forms.ModelForm):  
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'requisitos', 'quantidade_vagas', 'fim_candidaturas', 'area']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'max_length': 100}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'max_length': 5000}),
            'requisitos': forms.Textarea(attrs={'class': 'form-control', 'max_length': 5000}),
            'quantidade_vagas': forms.NumberInput(attrs={'class':'form-control', 'max': 100}),
            'fim_candidaturas': forms.DateInput(attrs={'type':'date', 'initial': datetime.date.today}),
            'area': forms.Select(choices=Vaga.AREAS, attrs={'class':'form-control'})
        }
    
    def clean_fim_candidaturas(self):
        fim_candidaturas = self.cleaned_data['fim_candidaturas']
        if fim_candidaturas < datetime.date.today():
            raise ValidationError(_('Fim de candidaturas deve ser a partir de hoje.'), code='invalido')
        return fim_candidaturas
    
    def clean_quantidade_vagas(self):
        quantidade_vagas = self.cleaned_data['quantidade_vagas']
        if quantidade_vagas < qnt_candidatos_selecionados(self.instance.id):
            raise ValidationError(_('A quantidade de vagas não pode ser menor que a quantidade de candidatos aprovados.'), code='invalido')
        return quantidade_vagas

class EditarVagaForm(VagaForm):

    class Meta(VagaForm.Meta):
        pass
    
    def __init__(self, *args, **kwargs):
        id_vaga = kwargs.pop('id_vaga', None)
        super().__init__(*args, **kwargs)

        if possui_candidatura(id_vaga):
            self.fields['titulo'].disabled = True
            self.fields['descricao'].disabled = True
            self.fields['requisitos'].disabled = True