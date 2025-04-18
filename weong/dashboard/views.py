from django.core import serializers
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from pytz import timezone as tz
import folium
import folium.raster_layers
import json

from utils.charts import meses, get_meses, cor_primaria
from usuario.models import Ong
from vaga.models import Vaga, Candidatura

sao_paulo = tz('America/Sao_Paulo')

def mapa_ongs(request: HttpRequest):
    map = folium.Map((-23.5449796, -46.6486328)) # Centro de São Paulo
    
    ongs = Ong.objects.filter(status='Ativa').all()
    if ongs:
        coordenadas = []
        for ong in ongs:
            coordenadas.append((ong.endereco.latitude, ong.endereco.longitude))
    
        for coordenada in coordenadas:
            folium.Marker(coordenada).add_to(map)
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

def chart_vagas(request: HttpRequest):
    return render(request, 'dashboard/chart_vagas.html', {})

def vagas_data(request: HttpRequest):
    vagas_preenchidas = Vaga.objects.filter(preenchida=True).all()
    num_vagas_preenchidas = 0
    for vaga in vagas_preenchidas:
        num_vagas_preenchidas += vaga.quantidade_vagas
    
    vagas_abertas = Vaga.objects.filter(preenchida=False).all()
    num_vagas_abertas = 0
    for vaga in vagas_abertas:
        num_vagas_abertas += vaga.quantidade_vagas
    
    dataset = {
        'num_vagas_preenchidas': num_vagas_preenchidas,
        'num_vagas_abertas': num_vagas_abertas
    }

    # data = serializers.serialize('json', dataset)
    return JsonResponse(json.loads(json.dumps(dataset)), safe=False)