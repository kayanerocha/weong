from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from brasilapy import BrasilAPI
from brasilapy.constants import APIVersion
from brasilapy.exceptions import ProcessorException
from validate_docbr import CNPJ, CPF
from datetime import date

from .models import Ong, Voluntario
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

class CadastroVoluntarioForm(forms.ModelForm):
    nome_completo=forms.CharField(max_length=255, label='Nome Completo')
    telefone = forms.CharField(max_length=11, label='Telefone')
    cpf = forms.CharField(max_length=11, label='CPF')
    data_nascimento = forms.DateField(label='Data de Nascimento', widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Voluntario
        fields = [
            'nome_completo',
            'telefone',
            'cpf',
            'data_nascimento',
        ]

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf_valido = CPF()
        if not cpf_valido.validate(cpf):
            raise ValidationError(_('CPF inválido.'), code='invalido')
        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        ddd = telefone[:2]
        try:
            client.get_ddd(ddd).dict()
        except ProcessorException:
            raise ValidationError(_('Número de telefone inválido.'), code='invalido')
        return telefone

    def clean_data_nascimento(self):
        try:
            data_nascimento = self.cleaned_data.get('data_nascimento')
            if not data_nascimento:
                raise ValidationError(_('Data de nascimento obrigatória.'), code='obrigatorio')

            hoje = date.today()
            idade = hoje.year - data_nascimento.year

            if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
                idade -= 1
            if idade < 18:
                raise ValidationError(_('Você deve ter pelo menos 18 anos para se cadastrar.'), code='idade_insuficiente')

            return data_nascimento

        except ValidationError as e:
            raise e  # Se for um erro esperado, apenas repassa

        except Exception as e:
            raise ValidationError(_('Erro ao validar a data de nascimento. Tente novamente.'), code='erro_interno')

class EditarOngForm(forms.ModelForm):
    class Meta:
        model = Ong
        fields = ['telefone', 'site']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class EditarVoluntarioForm(forms.ModelForm):
    class Meta:
        model = Voluntario
        fields = ['telefone']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)