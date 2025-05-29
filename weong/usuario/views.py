import cv2.data
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.files.base import ContentFile
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from verify_email.email_handler import ActivationMailManager
import base64
import cv2
import json
import numpy
import os

from usuario.forms import *
from usuario.models import *
from usuario.services import *
from vaga.models import Candidatura, Vaga

# Create your views here.

def cadastro_ong(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form_usuario = CadastroUsuarioForm(request.POST)
        form_ong = CadastroOngForm(request.POST)
        form_endereco = CadastroEnderecoForm(request.POST)
        
        if form_usuario.is_valid() and form_ong.is_valid() and form_endereco.is_valid() and form_endereco.endereco_consultado['descricao_situacao_cadastral'].upper() == 'ATIVA':
            usuario = form_usuario.save(commit=False)
            usuario.set_password(form_usuario.cleaned_data['password'])

            try:
                usuario = ActivationMailManager().send_verification_link(inactive_user=usuario, form=form_usuario, request=request)
            except Exception: # O servidor de email pode ficar indisponível por ser de teste
                usuario.is_active = False
                usuario.save()

            endereco = form_endereco.save()
            
            ong = form_ong.save(commit=False)
            ong.status_cnpj = form_ong.cnpj_consultado['descricao_situacao_cadastral']
            ong.usuario = usuario
            ong.endereco = endereco
            ong.save()

            messages.success(request, _('Cadastro realizado com sucesso! Aguarde ser validado.'))
            return redirect('cadastro-ong')
        else:
            messages.error(request, _('Erro no cadastro. Verifique os dados informados.'))
            if form_endereco.endereco_consultado['descricao_situacao_cadastral'].upper() != 'ATIVA':
                messages.error(request, _('Situação cadastral de ONG irregular.'))
    else:
        form_usuario = CadastroUsuarioForm()
        form_ong = CadastroOngForm()
        form_endereco = CadastroEnderecoForm()
    return render(request, 'registration/cadastro-ong.html', {
        'form_usuario': form_usuario,
        'form_ong': form_ong,
        'form_endereco': form_endereco,
    })

def cadastro_voluntario(request: HttpRequest):
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
            
            try:
                usuario = ActivationMailManager().send_verification_link(inactive_user=usuario, form=form_usuario, request=request)
            except Exception: # O servidor de email pode ficar indisponível por ser de teste
                usuario.is_active = False
                usuario.save()

            # Criar o endereço
            endereco = form_endereco.save()

            # Criar o voluntário
            voluntario = form_voluntario.save(commit=False)
            voluntario.usuario = usuario
            voluntario.endereco = endereco
            voluntario.save()

            messages.success(request, _('Cadastro realizado com sucesso!'))
            request.session['id_usuario'] = usuario.id
            request.session['acesso_autorizado'] = True
            return redirect('reconhecimento-facial')
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

def reconhecimento_facial(request: HttpRequest):
    if not request.session.get('acesso_autorizado'):
        return redirect('/')
    return render(request, 'registration/reconhecimento_facial.html')

@csrf_exempt
def post_reconhecimento_facial(request: HttpRequest):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            imagem_base64 = data['imagem'].split(',')[1]
            imagem_bytes = base64.b64decode(imagem_base64)
            imagem_numpy = numpy.frombuffer(imagem_bytes, numpy.uint8)

            frame = cv2.imdecode(imagem_numpy, cv2.IMREAD_COLOR)

            vivacidade = verificar_vivacidade(frame)
            fraude = detectar_fraude(frame)
            reflexo = verificar_reflexo(frame)
            textura = verificar_textura(frame)
            bordas_artificiais = detectar_bordas_artificiais(frame)

            if vivacidade and not fraude and not reflexo and not textura and not bordas_artificiais:
                nome_arquivo = f'reconhecimento_facial_{timezone.now().strftime("%d%m%Y%H%M%S")}.jpg'
                arquivo_django = ContentFile(imagem_bytes, name=nome_arquivo)
                
                ReconhecimentoFacial.objects.create(
                    imagem=arquivo_django,
                    vivacidade=vivacidade,
                    fraude=fraude,
                    reflexo=reflexo,
                    textura=textura,
                    bordas_artificiais=bordas_artificiais,
                    usuario=User.objects.filter(id=request.session['id_usuario']).get()
                )
                del request.session['id_usuario']
                del request.session['acesso_autorizado']
            
            return JsonResponse({
                'vivacidade': bool(vivacidade),
                'fraude': bool(fraude),
                'reflexo': bool(reflexo),
                'textura': bool(textura),
                'bordas_artificiais': bool(bordas_artificiais),
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Requisição inválida'}, status=400)

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
    endereco_form = None
    if ong:
        form_ong = EditarOngForm(instance=ong)
        # endereco_form = EditarEnderecoForm(instance=ong.endereco if ong.endereco else None)
    elif voluntario:
        form_voluntario = EditarVoluntarioForm(instance=voluntario)
        endereco_form = EditarEnderecoForm(instance=voluntario.endereco if voluntario.endereco else None)

    # 🔁 Se for submissão de formulário
    if request.method == "POST":
        form_usuario = EditarUsuarioForm(request.POST, instance=usuario)
        print(form_usuario.errors)
        if form_usuario.is_valid():
            if ong:
                form_ong = EditarOngForm(request.POST, instance=ong)
                print(form_ong.errors)
                if form_ong.is_valid():
                    usuario = form_usuario.save()
                    perfil = form_ong.save(commit=False)
                    
                    perfil.usuario = usuario
                    perfil.save()
                    
                    messages.success(request, "Perfil atualizado com sucesso!")
                    return redirect('perfil_usuario')
            elif voluntario:
                form_voluntario = EditarVoluntarioForm(request.POST, instance=voluntario)
                endereco_form = EditarEnderecoForm(request.POST, instance=voluntario.endereco if voluntario.endereco else None)
                print(endereco_form.errors)
                if form_voluntario.is_valid() and endereco_form.is_valid():
                    usuario = form_usuario.save()
                    endereco = endereco_form.save()
                    perfil = form_voluntario.save(commit=False)

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

class DetalheVoluntarioView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'usuario.view_voluntario'
    model = Voluntario

    def get(self, request, *args, **kwargs):
        id_voluntario = kwargs.get('pk')
        vagas_ong = Vaga.objects.filter(ong_id=request.user.id).all()
        for vaga in vagas_ong:
            candidaturas = Candidatura.objects.filter(vaga_id=vaga.id).all()
            for candidatura in candidaturas:
                if candidatura.voluntario.id == id_voluntario:
                    return super().get(request, *args, **kwargs)
        return redirect('minhas-vagas')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

@login_required
def revalidar_cnpj(request: HttpRequest, cnpj: str):
    ong = Ong.objects.filter(cnpj=cnpj)
    if not ong:
        messages.error(request, _('Não foi possível processar a sua solicitação.'))
        return redirect('perfil_usuario')

    ong = ong.get()
    if ong.usuario != request.user:
        messages.error(request, _('Não foi possível processar a sua solicitação.'))
        return redirect('perfil_usuario')
    
    try:
        cnpj_consultado = consultar_cnpj(cnpj)
        ong.nome_fantasia = cnpj_consultado['nome_fantasia']
        ong.razao_social = cnpj_consultado['razao_social']
        ong.status_cnpj = cnpj_consultado['descricao_situacao_cadastral']
        ong.endereco.logradouro = f'{cnpj_consultado["descricao_tipo_de_logradouro"]} {cnpj_consultado["logradouro"]}'
        ong.endereco.numero = cnpj_consultado['numero']
        ong.endereco.bairro = cnpj_consultado['bairro']
        ong.endereco.complemento = cnpj_consultado['complemento']
        ong.endereco.cidade = cnpj_consultado['municipio']
        ong.endereco.estado = cnpj_consultado['uf']
        ong.endereco.cep = cnpj_consultado['cep']
        ong.endereco.save()
        ong.save()
    except Exception as e:
        messages.error(request, _('Erro ao atualizar dados do CNPJ.'))
        return redirect('perfil_usuario')
    messages.success(request, _('Dados do CNPJ atualizados com sucesso.'))
    return redirect('perfil_usuario')

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('perfil_usuario')

    def form_valid(self, form):
        messages.success(request=self.request, message='Senha alterada com sucesso!')
        return super().form_valid(form)