from django.urls import path
from .views import *

urlpatterns = [
    path('mapa-ongs/', mapa_ongs, name='mapa-ongs'),
    path('estatisticas/', estatisticas, name='estatisticas'),
    path('chart-vagas/', chart_vagas, name='chart-vagas'),
    path('vagas-data/', vagas_data, name='vagas-data'),
    path('opcoes/', get_opcao, name='opcoes'),
    path('candidaturas-chart/<int:ano>/', get_candidaturas_chart, name='candidaturas-chart'),
]