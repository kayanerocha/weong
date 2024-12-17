from django.urls import path
from vaga import views

urlpatterns = [
    path('', views.index, name='index'),
]