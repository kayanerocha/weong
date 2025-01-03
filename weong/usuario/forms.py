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

        




