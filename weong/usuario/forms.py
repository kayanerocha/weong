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

from .models import Ong, Voluntario
from vaga.models import Endereco
from vaga.services import possui_candidatura

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
        if len(password) < 8 or not (any(not c.isalnum() for c in password) and (not password.isnumeric() and not password.isalpha() and not password.isspace())):
            self.add_error('password', 'A senha precisa ter no mínimo 8 caracteres com letras e números e pelo menos um caractere especial.')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Senhas divergentes')
        
        return cleaned_data

class CadastroEnderecoForm(forms.ModelForm):
    logradouro = forms.CharField(max_length=255, label='Logradouro', widget=forms.TextInput(attrs={'class':'form-control'}))
    numero = forms.CharField(max_length=20, label='Número', widget=forms.TextInput(attrs={'class':'form-control'}))
    complemento = forms.CharField(max_length=255, label='Complemento', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    bairro = forms.CharField(max_length=255, label='Bairro', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    cidade = forms.CharField(max_length=255, label='Cidade', widget=forms.TextInput(attrs={'class':'form-control'}))
    estado = forms.CharField(widget=forms.Select(choices=Endereco.ESTADOS, attrs={'class':'form-control'}), label='Estado')
    cep = forms.CharField(max_length=8, label='CEP', widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Endereco
        fields = ['logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']
    
    def clean_cep(self):
        cep = self.cleaned_data['cep']
        try:
            client.get_cep(cep, APIVersion.V1)
        except (ProcessorException, TypeError):
            try:
                client.get_cep(cep, APIVersion.V2)
            except (ProcessorException, TypeError):
                raise ValidationError(_('CEP não encontrado.'), code='invalido')    
        return cep

class EditarEnderecoForm(CadastroEnderecoForm):
    
    class Meta(CadastroEnderecoForm.Meta):
        pass

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