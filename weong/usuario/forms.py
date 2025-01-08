from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from validate_docbr import CNPJ

from .models import Ong
from vaga.models import Endereco

class CadastroUsuarioForm(forms.ModelForm):
    username = forms.CharField(min_length=3, max_length=150, label='Usuário')
    email = forms.EmailField(max_length=255, label='E-mail', validators=[EmailValidator(_('E-mail inválido, corrija.'))])
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirme a senha')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Senhas divergentes')
        
        return cleaned_data

class CadastroEnderecoForm(forms.ModelForm):
    logradouro = forms.CharField(max_length=255, label='Logradouro')
    numero = forms.CharField(max_length=20, label='Número')
    complemento = forms.CharField(max_length=255, label='Complemento', required=False)
    bairro = forms.CharField(max_length=255, label='Bairro', required=False)
    cidade = forms.CharField(max_length=255, label='Cidade')
    estado = forms.CharField(widget=forms.Select(choices=Endereco.ESTADOS), label='Estado')
    cep = forms.CharField(max_length=10, label='CEP')

    class Meta:
        model = Endereco
        fields = ['logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']

class CadastroOngForm(forms.ModelForm):
    nome_fantasia = forms.CharField(max_length=255, label='Nome Fantasia')
    razao_social = forms.CharField(max_length=255, required=False, label='Razão Social')
    cnpj = forms.CharField(min_length=14, max_length=14, label='CNPJ')
    telefone = forms.CharField(min_length=11, max_length=11, label='Telefone')
    site = forms.URLField(max_length=255, required=False, label='Site', validators=[URLValidator()])

    class Meta:
        model = Ong
        fields = ['nome_fantasia', 'razao_social', 'cnpj', 'telefone', 'site']

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        cnpj_valido = CNPJ()
        if not cnpj_valido.validate(cnpj):
            raise ValidationError(_('CNPJ inválido.'), code='invalido')
        return cnpj
    
    def clean_telefone(self):
        DDDS = (
            61, 62, 64, 65, 66, 67, # centro oeste
            82, 71, 73, 74, 75, 77, 85, 88, 98, 99, 83, 82, 87, 86, 89, 84, 79, # nordeste
            68, 96, 92, 97, 91, 93, 94, 69, 95, 63, # Norte
            27, 28, 31, 31, 33, 34, 35, 37, 38, 21, 22, 24, 11, 12, 13, 14, 15, 16, 17, 18, 19, # Sudeste
            41, 42, 43, 44, 45, 46, # Sul
        )
        telefone = self.cleaned_data['telefone']
        ddd = telefone[:2]
        if int(ddd) not in DDDS:
            raise ValidationError(_('Número de telefone inválido.'), code='invalido')
        return telefone

        




