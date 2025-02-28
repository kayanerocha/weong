from django.contrib.auth.decorators import login_required
from django.urls import path

from vaga.views import *
from vaga.views_candidaturas import *

urlpatterns = [
    path('', VagaList.as_view(), name='index'),
    path('lista-vagas/', VagaList.as_view(), name='lista-vagas'),
    path('detalhe-vaga/<int:pk>', DetalheVagaView.as_view(), name='detalhe-vaga'),
    path('cadastro-vaga/', login_required(VagaCreate.as_view()), name='cadastro-vaga'),
    path('editar-vaga/<int:pk>', login_required(VagaUpdate.as_view()), name='edita-vaga'),
    path('minhas-vagas/', login_required(MinhasVagasList.as_view()), name='minhas-vagas'),
    path('deletar-vaga/<int:pk>', login_required(VagaDelete.as_view()), name='deletar-vaga'),
    path('candidatarse/<int:pk>', criar_candidatura, name='candidatarse'),
    path('minhas-candidaturas/', MinhasCandidaturas.as_view(), name='minhas-candidaturas'),
]