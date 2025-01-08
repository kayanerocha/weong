from django.urls import path
from usuario import views

urlpatterns = [
    path('cadastro-ong', views.cadastro_ong, name='cadastro-ong'),
]