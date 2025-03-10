from django.urls import path
from usuario import views
from usuario.views import cadastro_voluntario, perfil_usuario

urlpatterns = [
    path('cadastro-ong/', views.cadastro_ong, name='cadastro-ong'),
    path('cadastro-voluntario/', cadastro_voluntario, name='cadastro-voluntario'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
]