from django.urls import path

from vaga import views

urlpatterns = [
    path('', views.ListaVagasView.as_view(), name='index'),
    path('lista-vagas/', views.ListaVagasView.as_view(), name='lista-vagas'),
    path('detalhe-vaga/<int:pk>', views.DetalheVagaView.as_view(), name='detalhe-vaga'),
    path('cadastro-vaga/', views.cadastrar_vaga, name='cadastro-vaga'),
    path('editar-vaga/<int:pk>', views.editar_vaga, name='edita-vaga')
]