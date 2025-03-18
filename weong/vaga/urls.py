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
    path('minhas-candidaturas/', login_required(MinhasCandidaturas.as_view()), name='minhas-candidaturas'),
    path('cancelar-candidatura/<int:pk>', cancelar_candidatura, name='cancelar-candidatura'),
    path('aprovar-candidato/<int:id_candidatura>', aprovar_candidato, name='aprovar-candidato'),
    path('reprovar-candidato/<int:id_candidatura>', reprovar_candidato, name='reprovar-candidato'),
    path('preencher-vaga/<int:pk>', preencher_vaga, name='preencher-vaga'),
]