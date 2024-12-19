from django.urls import path
from vaga import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vagas/<int:pk>', views.DetalheVagaView.as_view(), name='detalhe-vaga'),
]