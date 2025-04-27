from datetime import date
from django import forms
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from brasilapy import BrasilAPI
from brasilapy.constants import APIVersion
from brasilapy.models.cnpj import CNPJ as Cnpj
from brasilapy.exceptions import ProcessorException
from validate_docbr import CNPJ, CPF

from .models import Ong, Voluntario
from .services import *
from vaga.models import Endereco
from vaga.services import possui_candidatura

client = BrasilAPI()

class CadastroUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'type': 'text', 'min_length': 3, 'max_length': 150, 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'type': 'email', 'max_length': 255, 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control'}),
            'password_confirm': forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control'}),
        }

    def clean_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if len(password) < 8 or not (any(not c.isalnum() for c in password) and (not password.isnumeric() and not password.isalpha() and not password.isspace())):
            self.add_error('password', 'A senha precisa ter no mínimo 8 caracteres com letras e números e pelo menos um caractere especial.')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Senhas divergentes.')
        
        return password

class CadastroEnderecoForm(forms.ModelForm):
    logradouro = forms.CharField(max_length=255, label='Logradouro', widget=forms.TextInput(attrs={'class':'form-control'}))
    numero = forms.CharField(max_length=20, label='Número', widget=forms.TextInput(attrs={'class':'form-control'}))
    complemento = forms.CharField(max_length=255, label='Complemento', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    bairro = forms.CharField(max_length=255, label='Bairro', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    cidade = forms.CharField(max_length=255, label='Cidade', widget=forms.TextInput(attrs={'class':'form-control'}))
    estado = forms.CharField(widget=forms.Select(choices=Endereco.ESTADOS, attrs={'class':'form-control', 'id': 'estado', 'readonly': True}), label='Estado')
    cep = forms.CharField(max_length=8, label='CEP', widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Endereco
        fields = ['logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endereco_consultado = None
        if 'cnpj' in self.data.keys():
            self.endereco_consultado = consultar_cnpj(self.data['cnpj'])
        elif 'cep' in self.data.keys():
            self.endereco_consultado = consultar_cep(self.data['cep'])    
    
    def clean_logradouro(self):
        logradouro = self.cleaned_data['logradouro']
        if self.endereco_consultado:
            if 'cnpj' in self.data.keys():
                if logradouro != f'{self.endereco_consultado['descricao_tipo_de_logradouro']} {self.endereco_consultado['logradouro']}':
                    raise ValidationError(_('Logradouro inconsistente.'), code='invalido')
            else:
                if logradouro != self.endereco_consultado['street']:
                    raise ValidationError(_('Logradouro inconsistente.'), code='invalido')
            
        return logradouro
    
    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if 'cnpj' in self.data.keys() and self.endereco_consultado and numero != self.endereco_consultado['numero']:
            raise ValidationError(_('Número de endereço inconsistente.', code='invalido'))
        return numero
    
    def clean_bairro(self):
        bairro = self.cleaned_data['bairro']
        if self.endereco_consultado:
            if 'cnpj' in self.data.keys():
                if bairro != self.endereco_consultado['bairro']:
                    raise ValidationError(_('Bairro inconsistente.'), code='invalido')
            else:
                if bairro != self.endereco_consultado['neighborhood']:
                    raise ValidationError(_('Bairro inconsistente.'), code='invalido')
        return bairro

    def clean_complemento(self):
        complemento = self.cleaned_data['complemento']
        if 'cnpj' in self.data.keys() and self.endereco_consultado and complemento != self.endereco_consultado['complemento']:
            raise ValidationError(_('Complemento inconsistente.'), code='invalido')
        return complemento
    
    def clean_cidade(self):
        cidade = self.cleaned_data['cidade']
        if self.endereco_consultado:
            if 'cnpj' in self.data.keys():
                if cidade != self.endereco_consultado['municipio']:
                    raise ValidationError(_('Município inconsistente.'), code='invalido')
            else:
                if cidade != self.endereco_consultado['city']:
                    raise ValidationError(_('Município inconsistente.'), code='invalido')
        return cidade
    
    def clean_estado(self):
        estado = self.cleaned_data['estado']
        if self.endereco_consultado:
            if 'cnpj' in self.data.keys():
                if estado != self.endereco_consultado['uf']:
                    raise ValidationError(_('Estado inconsistente.'), code='invalido')
            else:
                if estado != self.endereco_consultado['state']:
                    raise ValidationError(_('Estado inconsistente.'), code='invalido')
        return estado
    
    def clean_cep(self):
        cep = self.cleaned_data['cep']
        
        try:
            client.get_cep(cep, APIVersion.V1)
        except (ProcessorException, TypeError):
            try:
                client.get_cep(cep, APIVersion.V2)
            except (ProcessorException, TypeError):
                raise ValidationError(_('CEP não encontrado.'), code='invalido')

        if self.endereco_consultado:
            logradouro = self.data['logradouro']
            if 'cnpj' in self.data.keys():
                if cep != self.endereco_consultado['cep']:
                    raise ValidationError(_('CEP inconsistente.'), code='invalido')
            else:
                if logradouro != self.endereco_consultado['street']:
                    raise ValidationError(_('CEP inconsistente.'), code='invalido')
        return cep

class EditarEnderecoForm(CadastroEnderecoForm):
    
    class Meta(CadastroEnderecoForm.Meta):
        pass

class CadastroOngForm(forms.ModelForm):
    class Meta:
        model = Ong
        fields = ['nome_fantasia', 'razao_social', 'cnpj', 'telefone', 'site']
        widgets = {
            'cnpj': forms.TextInput(attrs={'type': 'text', 'min_length': 14, 'max_length': 14, 'class':'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'type': 'text', 'max_length': 255, 'class':'form-control'}),
            'razao_social': forms.TextInput(attrs={'type': 'text', 'max_length': 255, 'required': False, 'class':'form-control'}),
            'telefone': forms.TextInput(attrs={'type': 'text', 'min_length': 11, 'max_length': 11, 'class':'form-control'}),
            'site': forms.URLInput(attrs={'type': 'text', 'max_length': 255, 'required': False, 'class':'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cnpj_consultado = None
        if 'cnpj' in self.data.keys():
            cnpj = self.data['cnpj']
            self.cnpj_consultado = consultar_cnpj(cnpj)

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        if not self.cnpj_consultado:
            raise ValidationError(_('CNPJ inválido.'), code='invalido')
        return cnpj
    
    def clean_nome_fantasia(self):
        nome_fantasia = self.cleaned_data['nome_fantasia']

        if not self.cnpj_consultado:
            return nome_fantasia
        
        if nome_fantasia and nome_fantasia != self.cnpj_consultado['nome_fantasia']:
            raise ValidationError(_('Nome da ONG inconsistente.'), code='invalido')
        return nome_fantasia
    
    def clean_razao_social(self):
        razao_social = self.cleaned_data['razao_social']

        if not self.cnpj_consultado:
            return razao_social

        if razao_social != self.cnpj_consultado['razao_social']:
            raise ValidationError(_('Razão social inconsistente.'), code='invalido')
        return razao_social
    
    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        ddd = telefone[:2]
        try:
            client.get_ddd(ddd).dict()
        except ProcessorException as e:
            raise ValidationError(_('Número de telefone inválido.'), code='invalido')
        return telefone

class CadastroVoluntarioForm(forms.ModelForm):
    class Meta:
        model = Voluntario
        fields = [
            'nome_completo',
            'telefone',
            'cpf',
            'data_nascimento',
        ]
        widgets = {
            'nome_completo': forms.TextInput(attrs={'type': 'text', 'max_length': 255, 'class':'form-control'}),
            'telefone': forms.TextInput(attrs={'type': 'text', 'max_length': 11, 'class':'form-control'}),
            'cpf': forms.TextInput(attrs={'type': 'text', 'max_length': 11, 'class':'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        }

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

class EditarUsuarioForm(CadastroUsuarioForm):
    class Meta(CadastroUsuarioForm.Meta):
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def clean_password(self):
        return

class EditarOngForm(CadastroOngForm):
    class Meta(CadastroOngForm.Meta):
        fields = ['telefone', 'site']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class EditarVoluntarioForm(CadastroVoluntarioForm):
    class Meta(CadastroVoluntarioForm.Meta):
        fields = CadastroVoluntarioForm.Meta.fields[:]
        fields.append('status')
        widgets = CadastroVoluntarioForm.Meta.widgets
        widgets['status'] = forms.Select(choices=Voluntario.STATUS_VOLUNTARIO, attrs={'class':'form-control'})
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['cpf'].disabled = True
        self.fields['status'].disabled = True

class EditarEnderecoForm(CadastroEnderecoForm):
    class Meta(CadastroEnderecoForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'cnpj' in self.data:
            self.fields = []

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        if request.method == 'POST':
            if not request.user.is_active:
                messages.error(request, 'Usuário inativo ou senha incorreta. Aguarde a aprovação ou altere a sua senha.')
            
        