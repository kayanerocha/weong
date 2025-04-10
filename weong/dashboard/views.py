from django.shortcuts import render
from django.http import HttpRequest
import folium
import folium.raster_layers

from usuario.models import Ong

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
    # return render(request, 'dashboard/mapa_ongs.html', {'ongs': ongs})