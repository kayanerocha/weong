from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from validate_docbr import CNPJ

class CadastroOngForm(forms.Form):
    nome_fantasia = forms.CharField(max_length=255, label='Nome Fantasia')
    razao_social = forms.CharField(max_length=255, required=False, label='Razão Social')
    cnpj = forms.CharField(min_length=14, max_length=14, label='CNPJ')
    telefone = forms.CharField(min_length=11, max_length=11, label='Telefone')
    email = forms.EmailField(max_length=255, label='E-mail', validators=[EmailValidator(_('E-mail inválido, corrija.'))])
    site = forms.URLField(max_length=255, required=False, label='Site', validators=[URLValidator()])
    senha = forms.PasswordInput()

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        cnpj_valido = CNPJ()
        if not cnpj_valido.validate(cnpj):
            raise ValidationError(_('CNPJ inválido, corrija.'))
        return cnpj
    
    def clean_telefone(self):
        ddd = self.cleaned_data['telefone'][:2]

        




