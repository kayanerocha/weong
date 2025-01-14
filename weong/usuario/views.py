from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import generic

from usuario.forms import CadastroUsuarioForm, CadastroOngForm, CadastroEnderecoForm
from usuario.models import Ong

# Create your views here.


def cadastro_ong(request):
    if request.method == 'POST':
        form_usuario = CadastroUsuarioForm(request.POST)
        form_ong = CadastroOngForm(request.POST)
        form_endereco = CadastroEnderecoForm(request.POST)
        
        if form_usuario.is_valid() and form_ong.is_valid() and form_endereco.is_valid():
            usuario = form_usuario.save(commit=False)
            usuario.set_password(form_usuario.cleaned_data['password'])
            usuario.is_active = False
            usuario.save()

            endereco = form_endereco.save()
            
            ong = form_ong.save(commit=False)
            ong.usuario = usuario
            ong.endereco = endereco
            ong.save()

            return redirect('/')
        else:
            messages.error(request, _('Cadastro não realizado.'))
    else:
        form_usuario = CadastroUsuarioForm()
        form_ong = CadastroOngForm()
        form_endereco = CadastroEnderecoForm()
    return render(request, 'cadastro-ong.html', {
        'form_usuario': form_usuario,
        'form_ong': form_ong,
        'form_endereco': form_endereco,
    })

class CadastroOngView(generic.CreateView):
    model = Ong
    form_class = CadastroOngForm