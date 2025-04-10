from django.urls import path
from .views import mapa_ongs

urlpatterns = [
    path('mapa-ongs', mapa_ongs, name='mapa-ongs'),
]