from django.urls import path
from usuario import views

urlpatterns = [
    path('ong/<str:username>/cadastro/', views.cadastro_ong, name='cadastro-ong'),
]