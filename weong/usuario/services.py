from decouple import config
from django.core.cache import cache
from django.core.mail import send_mail
from django.template import loader
from time import sleep
from validate_docbr import CNPJ
import requests

def cnpj_valido(cnpj: str) -> bool:
    cnpj_valido = CNPJ()
    if not cnpj_valido.validate(cnpj):
        return False
    return True

def consultar_cnpj(cnpj: str):
    if not cnpj_valido(cnpj):
        print('entrou no inválido')
        return None

    cache_data = cache.get(cnpj)
    if cache_data:
        return cache_data
    
    try:
        response = requests.get(f'{config("URL_BRASIL_API")}cnpj/v1/{cnpj}')
    except Exception as e:
        print(e)
        return None
    else:
        if response.status_code == 200:
            cache.set(cnpj, response.json(), timeout=60 * 15)
            return response.json()
        if response.status_code == 429:
            sleep(10)
            consultar_cnpj(cnpj)

def consultar_cep(cep: str):
    cache_data = cache.get(cep)
    if cache_data:
        return cache_data
    
    try:
        response = requests.get(f'{config("URL_BRASIL_API")}cep/v2/{cep}')
    except Exception:
        return None
    else:
        if response.status_code == 200:
            cache.set(cep, response.json(), timeout=60*15)
            return response.json()
        if response.status_code == 429:
            sleep(10)
            consultar_cep(cep)

def enviar_resultado_analise(status: str, destinatario: str):
    resultado = 'aprovado' if status == 'Ativa' else 'reprovado'
    send_mail(
            'Resultado da Análise de Perfil',
            f'Seu perfil foi {resultado}',
            'kayanerocha.ti@gmail.com',
            [destinatario],
            fail_silently=False,
            # html_message=loader.render_to_string('emails/analise_perfil.html', {'resultado': resultado})
        )