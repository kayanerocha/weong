from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from brasilapy import BrasilAPI
from brasilapy.constants import APIVersion
from brasilapy.exceptions import ProcessorException
from validate_docbr import CNPJ

from .models import Ong
from vaga.models import Endereco

client = BrasilAPI()

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
    cep = forms.CharField(max_length=8, label='CEP')

    class Meta:
        model = Endereco
        fields = ['logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']
    
    def clean_cep(self):
        cep = self.cleaned_data['cep']
        try:
            client.get_cep(cep, APIVersion.V1)
        except ProcessorException:
            try:
                client.get_cep(cep, APIVersion.V2)
            except ProcessorException:
                raise ValidationError(_('CEP não encontrado.'), code='invalido')    
        return cep

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
        telefone = self.cleaned_data['telefone']
        ddd = telefone[:2]
        try:
            client.get_ddd(ddd).dict()
        except ProcessorException as e:
            raise ValidationError(_('Número de telefone inválido.'), code='invalido')
        return telefone