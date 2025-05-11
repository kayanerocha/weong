from django.contrib.auth.views import LoginView
from django.urls import path
from usuario import views
from usuario.views import *

urlpatterns = [
    path('cadastro-ong/', views.cadastro_ong, name='cadastro-ong'),
    path('cadastro-voluntario/', cadastro_voluntario, name='cadastro-voluntario'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('login/', LoginView.as_view(), name='login'),
    path('alterar-senha/', CustomPasswordChangeView.as_view(), name='alterar-senha'),
    path('detalhe-ong/<int:pk>', DetalheOngView.as_view(), name='detalhe-ong'),
    path('detalhe-voluntario/<int:pk>', DetalheVoluntarioView.as_view(), name='detalhe-voluntario'),
    path('revalidar-cnpj/<str:cnpj>', revalidar_cnpj, name='revalidar-cnpj'),
]