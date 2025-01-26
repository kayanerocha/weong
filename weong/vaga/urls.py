from django.contrib.auth.decorators import login_required
from django.urls import path

from vaga.views import *

urlpatterns = [
    path('', VagaList.as_view(), name='index'),
    path('lista-vagas/', VagaList.as_view(), name='lista-vagas'),
    path('detalhe-vaga/<int:pk>', DetalheVagaView.as_view(), name='detalhe-vaga'),
    path('cadastro-vaga/', login_required(VagaCreate.as_view()), name='cadastro-vaga'),
    path('editar-vaga/<int:pk>', editar_vaga, name='edita-vaga'),
    path('minhas-vagas/', login_required(MinhasVagasList.as_view()), name='minhas-vagas')
]