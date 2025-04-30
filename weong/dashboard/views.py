from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from datetime import datetime
from pytz import timezone as tz
import folium
import folium.raster_layers

from utils.charts import *
from usuario.models import Ong, Voluntario
from vaga.models import Vaga, Candidatura
from .services import *

sao_paulo = tz('America/Sao_Paulo')

def mapa_ongs(request: HttpRequest):
    ip_usuario = get_ip_usuario(request)
    localizacao_usuario = get_localizacao_ip(ip_usuario)
    
    # Inicialmente as coordenadas do Centro de São Paulo
    latitude = -23.5449796
    longitude = -46.6486328
    if localizacao_usuario:
        latitude = localizacao_usuario['latitude']
        longitude = localizacao_usuario['longitude']

    map = folium.Map((latitude, longitude))
    
    ongs = Ong.objects.filter(status='Ativa').all()
    if ongs:
        coordenadas = []
        dados_ongs = []
        for ong in ongs:
            coordenadas.append((ong.endereco.latitude, ong.endereco.longitude))
            dados_ongs.append({
                'nome': ong.razao_social
            })

        for i, coordenada in enumerate(coordenadas):
            folium.Marker(coordenada, popup=f'<a href={ongs[i].get_absolute_url()} target="_blank">Acessar perfil</a>', tooltip=f'{ongs[i].razao_social}').add_to(map)
    folium.raster_layers.TileLayer(tiles='OpenStreetMap').add_to(map)
    folium.raster_layers.TileLayer(tiles='CartoDB Positron').add_to(map)
    folium.raster_layers.TileLayer(tiles='CartoDB Voyager').add_to(map)
    folium.LayerControl().add_to(map)

    map = map._repr_html_()
    context = {
        'map': map
    }
    return render(request, 'dashboard/mapa_ongs.html', context)

def get_opcao(request: HttpRequest):
    candidaturas_agrupadas = Candidatura.objects.annotate(year=ExtractYear('created_at')).values('year').order_by('-year').distinct()
    opcoes = [candidatura['year'] for candidatura in candidaturas_agrupadas]

    return JsonResponse({
        'opcoes': opcoes
    })

def get_candidaturas_chart(request: HttpRequest, ano: int):
    candidaturas = Candidatura.objects.filter(created_at__date__year=ano).values('created_at__date__month').annotate(num_candidaturas=Count('created_at__date__month')).order_by()
    
    meses_dict = get_meses()
    
    for candidatura in candidaturas:
        meses_dict[meses[candidatura['created_at__date__month']-1]] = candidatura['num_candidaturas']
    return JsonResponse({
        'title': f'Candidaturas realizadas em {ano}',
        'data': {
            'labels': list(meses_dict.keys()),
            'datasets': [{
                'label': 'Quantidade de Candidaturas',
                'backgroundColor': cor_primaria,
                'borderColor': cor_primaria,
                'data': list(meses_dict.values())
            }]
        }
    })

def estatisticas(request: HttpRequest):
    return render(request, 'dashboard/estatisticas.html', {})

def get_vagas_data(request: HttpRequest, ano: int):
    vagas = Vaga.objects.filter(created_at__date__year=ano)

    return JsonResponse({
        'title': f'Vagas cadastradas em {ano}',
        'data': {
            'labels': ['Abertas', 'Preenchidas'],
            'datasets': [{
                'label': 'Vagas',
                'backgroundColor': ['#97db4f', '#277348'],
                'borderColor': ['#97db4f', '#277348'],
                'data': [
                    vagas.filter(preenchida=1).count(),
                    vagas.filter(preenchida=0, fim_candidaturas__gte=datetime.now().date()).count(),
                ],
            }]
        },
    })

def get_usuarios_data(request: HttpRequest, ano: int):
    ongs = Ong.objects.filter(status='Ativa').count()
    voluntarios = Voluntario.objects.filter(status='Ativo').count()

    return JsonResponse({
        'title': f'Usuários cadastrados em {ano}',
        'data': {
            'labels': ['ONGs', 'Voluntários'],
            'datasets': [{
                'label': 'Usuários',
                'backgroundColor': [cor_primaria, '#547792'],
                'borderColor': [cor_primaria, '#547792'],
                'data': [
                    ongs,
                    voluntarios
                ],
            }]
        },
    })

def get_vagas_area_data(request: HttpRequest, ano: int):
    vagas_area = Vaga.objects.filter(created_at__date__year=ano).values('area').annotate(quantidade=Count('area')).order_by()

    areas_dict = get_areas()
    
    for area in vagas_area:
        areas_dict[area['area']] = area['quantidade']

    return JsonResponse({
        'title': f'Vagas por área em {ano}',
        'data': {
            'labels': list(areas_dict.keys()),
            'datasets': [{
                'label': 'Quantidade de Vagas',
                'backgroundColor': cores_areas,
                'borderColor': cores_areas,
                'data': list(areas_dict.values()),
            }]
        }
    })

def get_vagas_mes_data(request: HttpRequest, ano: int):
    vagas_mes = Vaga.objects.filter(created_at__date__year=ano).values('created_at__date__month').annotate(num_vagas=Count('created_at__date__month')).order_by()

    meses_dict = get_meses()

    for vaga in vagas_mes:
        meses_dict[meses[vaga['created_at__date__month']-1]] = vaga['num_vagas']
    
    return JsonResponse({
        'title': f'Vagas criadas em {ano}',
        'data': {
            'labels': list(meses_dict.keys()),
            'datasets': [{
                'label': 'Quantidade de Vagas',
                'backgroundColor': cor_primaria,
                'borderColor': cor_primaria,
                'data': list(meses_dict.values())
            }]
        }
    })