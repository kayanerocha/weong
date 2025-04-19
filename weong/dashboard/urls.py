from django.urls import path
from .views import *

urlpatterns = [
    path('mapa-ongs/', mapa_ongs, name='mapa-ongs'),
    path('estatisticas/', estatisticas, name='estatisticas'),
    path('opcoes/', get_opcao, name='opcoes'),
    path('candidaturas-chart/<int:ano>/', get_candidaturas_chart, name='candidaturas-chart'),
    path('vagas-chart/<int:ano>/', get_vagas_data, name='candidaturas-chart'),
]