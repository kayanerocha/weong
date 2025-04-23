from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required

from usuario.forms import *
from usuario.models import Ong, Voluntario

# Create your views here.


def cadastro_ong(request):
    if request.user.is_authenticated:
        return redirect('/')
    
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

            messages.success(request, _('Cadastro realizado com sucesso! Aguarde ser validado.'))
            return redirect('cadastro-ong')
        else:
            messages.error(request, _('Erro no cadastro. Verifique os dados informados.'))
    else:
        form_usuario = CadastroUsuarioForm()
        form_ong = CadastroOngForm()
        form_endereco = CadastroEnderecoForm()
    return render(request, 'registration/cadastro-ong.html', {
        'form_usuario': form_usuario,
        'form_ong': form_ong,
        'form_endereco': form_endereco,
    })

class CadastroOngView(generic.CreateView):
    model = Ong
    form_class = CadastroOngForm

def cadastro_voluntario(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form_usuario = CadastroUsuarioForm(request.POST)
        form_voluntario = CadastroVoluntarioForm(request.POST)
        form_endereco = CadastroEnderecoForm(request.POST)

        if form_usuario.is_valid() and form_voluntario.is_valid() and form_endereco.is_valid():
            # Criar o usuário
            usuario = form_usuario.save(commit=False)
            usuario.set_password(form_usuario.cleaned_data['password'])
            usuario.is_active = False
            usuario.save()

            # Criar o endereço
            endereco = form_endereco.save()

            # Criar o voluntário
            voluntario = form_voluntario.save(commit=False)
            voluntario.usuario = usuario
            voluntario.endereco = endereco
            voluntario.save()

            messages.success(request, _('Cadastro realizado com sucesso! Aguarde ser validado.'))
            return redirect('cadastro-voluntario')
        else:
            messages.error(request, _('Erro no cadastro. Verifique os dados informados.'))
    else:
        form_usuario = CadastroUsuarioForm()
        form_voluntario = CadastroVoluntarioForm()
        form_endereco = CadastroEnderecoForm()

    #Renderizar endereco
    return render(request, 'registration/cadastro-voluntario.html', {
        'form_usuario': form_usuario,
        'form_voluntario': form_voluntario,
        'form_endereco': form_endereco,
    })

class CadastroVoluntaioView(generic.CreateView):
    model = Voluntario
    form_class = CadastroVoluntarioForm

@login_required
def perfil_usuario(request):
    usuario = request.user
    ong = Ong.objects.filter(usuario=usuario).first()
    voluntario = Voluntario.objects.filter(usuario=usuario).first()

    # 🟡 Se não houver perfil vinculado, mostrar tela amigável
    if not ong and not voluntario:
        return render(request, 'registration/perfil_nao_configurado.html')

    # 🟢 Se houver perfil, carregar os formulários
    form_usuario = EditarUsuarioForm(instance=usuario)
    form_ong = None
    form_voluntario = None
    if ong:
        form_ong = EditarOngForm(instance=ong)
        endereco_form = CadastroEnderecoForm(instance=ong.endereco if ong.endereco else None)
    elif voluntario:
        form_voluntario = EditarVoluntarioForm(instance=voluntario)
        endereco_form = CadastroEnderecoForm(instance=voluntario.endereco if voluntario.endereco else None)

    # 🔁 Se for submissão de formulário
    if request.method == "POST":
        form_usuario = EditarUsuarioForm(request.POST, instance=usuario)
        if ong:
            form_ong = EditarOngForm(request.POST, instance=ong)
            endereco_form = CadastroEnderecoForm(request.POST, instance=ong.endereco if ong.endereco else None)
        elif voluntario:
            form_voluntario = EditarVoluntarioForm(request.POST, instance=voluntario)
            endereco_form = CadastroEnderecoForm(request.POST, instance=voluntario.endereco if voluntario.endereco else None)
        
        print(form_usuario.errors)
        print(form_ong.errors)
        print(endereco_form.errors)
        if form_usuario.is_valid() and (form_ong and form_ong.is_valid() or form_voluntario and form_voluntario.is_valid()) and endereco_form.is_valid():
            usuario = form_usuario.save()
            endereco = endereco_form.save()

            perfil = form_voluntario.save(commit=False) if form_voluntario else form_ong.save(commit=False)
            perfil.usuario = usuario
            perfil.endereco = endereco
            perfil.save()

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil_usuario')

    return render(request, 'registration/perfil.html', {
        'form_ong': form_ong,
        'form_usuario': form_usuario,
        'form_voluntario': form_voluntario,
        'endereco_form': endereco_form,
        'ong': ong,
        'voluntario': voluntario
    })

class DetalheOngView(generic.DetailView):
    model = Ong

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class DetalheVoluntarioView(generic.DetailView):
    model = Voluntario

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
