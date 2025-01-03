from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from usuario.forms import CadastroOngForm
from usuario.models import Ong

# Create your views here.

def cadastro_ong(request, username):
    if request.method == 'POST':
        ong = Ong.objects.get(user__username=username)
        return render(request, 'ong.html', {'ong': ong})