from decouple import config
from django.core.cache import cache
from django.core.mail import send_mail
from django.template import loader
from skimage.feature import local_binary_pattern
from time import sleep
from validate_docbr import CNPJ
import cv2
import numpy
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
    try:
        send_mail(
                'Resultado da Análise de Perfil',
                f'Seu perfil foi {resultado}',
                'kayanerocha.ti@gmail.com',
                [destinatario],
                fail_silently=False,
                # html_message=loader.render_to_string('emails/analise_perfil.html', {'resultado': resultado})
            )
    except Exception:
        pass

def verificar_vivacidade(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    std_dev = numpy.std(gray)
    return std_dev > 5

def detectar_fraude(frame):
    blur = cv2.Laplacian(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
    return blur < 50 

def verificar_reflexo(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < 100

def verificar_textura(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    lbp = local_binary_pattern(gray, 8, 1, method='uniform')
    hist, _ = numpy.histogram(lbp.ravel(), bins=numpy.arange(0, 59))
    uniformidade = numpy.std(hist)
    return uniformidade < 10

def detectar_bordas_artificiais(frame):
    edges = cv2.Canny(frame, 100, 200)
    contagem = numpy.sum(edges > 0)
    return contagem > 10000

def verificar_filtro_beleza(frame, face_bbox):
    x, y, w, h = face_bbox
    face = frame[y:y+h, x:x+w]
    hsv = cv2.cvtColor(face, cv2.COLOR_BGR2HSV)
    s = hsv[:, :, 1]
    return numpy.std(s) < 10
