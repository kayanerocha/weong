from django.urls import path

from vaga import views

urlpatterns = [
    path('', views.VagaList.as_view(), name='index'),
    path('lista-vagas/', views.VagaList.as_view(), name='lista-vagas'),
    path('detalhe-vaga/<int:pk>', views.DetalheVagaView.as_view(), name='detalhe-vaga'),
    path('cadastro-vaga/', views.VagaCreate.as_view(), name='cadastro-vaga'),
    path('editar-vaga/<int:pk>', views.editar_vaga, name='edita-vaga'),
    # path('teste-cadastro/', views.VagaCreate.as_view()),
    path('minhas-vagas/', views.MinhasVagasList.as_view(), name='minhas-vagas')
]