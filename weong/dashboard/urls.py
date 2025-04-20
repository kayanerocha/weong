from django.urls import path
from .views import *

urlpatterns = [
    path('mapa-ongs/', mapa_ongs, name='mapa-ongs'),
    path('estatisticas/', estatisticas, name='estatisticas'),
    path('opcoes/', get_opcao, name='opcoes'),
    path('candidaturas-chart/<int:ano>/', get_candidaturas_chart, name='candidaturas-chart'),
    path('vagas-chart/<int:ano>/', get_vagas_data, name='vagas-chart'),
    path('usuarios-chart/<int:ano>/', get_usuarios_data, name='usuarios-chart'),
    path('vagas-area-chart/<int:ano>/', get_vagas_area_data, name='vagas-area-chart'),
    path('vagas-mes-chart/<int:ano>/', get_vagas_mes_data, name='vagas-mes-chart'),
]