from django.urls import path
from usuario import views
from usuario.views import cadastro_voluntario, perfil_usuario, DetalheOngView, DetalheVoluntarioView

urlpatterns = [
    path('cadastro-ong/', views.cadastro_ong, name='cadastro-ong'),
    path('cadastro-voluntario/', cadastro_voluntario, name='cadastro-voluntario'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('detalhe-ong/<int:pk>', DetalheOngView.as_view(), name='detalhe-ong'),
    path('detalhe-voluntario/<int:pk>', DetalheVoluntarioView.as_view(), name='detalhe-voluntario'),
]