from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from datetime import datetime

from .models import Vaga, Candidatura
from .forms import *
from usuario.forms import CadastroEnderecoForm, EditarEnderecoForm
from usuario.models import Ong, Voluntario, Endereco
from .services import candidatos_selecionados, candidatura_existe, possui_candidatura

class ListaVagasView(generic.ListView):
    model = Vaga
    context_object_name = 'lista_vagas'

    def get_queryset(self):
        return Vaga.objects.filter(preenchida__exact=0, ong__status__exact='Inativa')
    
    def get_context_data(self, **kwargs):
        context = super(ListaVagasView, self).get_context_data(**kwargs)
        context['titulo'] = 'Vagas Abertas'
        return context
    
    template_name = 'vagas/lista.html'

class DetalheVagaView(generic.DetailView):
    model = Vaga

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_candidato'] = False
        context['candidaturas'] = []
        context['quantidade_candidatos'] = 0
        context['vagas_preenchidas'] = 0
        context['vagas_restantes'] = 0
        context['candidatos_selecionados'] = candidatos_selecionados(context['object'].id)
        context['vagas_preenchidas'] = candidatos_selecionados(context['object'].id)
        
        if self.request.user.is_authenticated:
            id_vaga = context['object'].id
            if Voluntario.objects.filter(usuario_id=self.request.user.id).exists():
                voluntario = Voluntario.objects.filter(usuario_id=self.request.user.id).get()
                if candidatura_existe(id_vaga, voluntario.id):
                    messages.info(self.request, _('Candidatura já realizada.'))
                    context['is_candidato'] = True
        
            if Ong.objects.filter(usuario_id=self.request.user.id).exists():
                candidaturas = Candidatura.objects.filter(vaga_id=id_vaga).all()
                context['candidaturas'] = candidaturas
                context['quantidade_candidatos'] = len(candidaturas)
                qnt_vagas_preenchidas = len(candidaturas.filter(status='Aceito'))
                context['qnt_vagas_preenchidas'] = qnt_vagas_preenchidas
                context['vagas_restantes'] = context['object'].quantidade_vagas - qnt_vagas_preenchidas
        return context

@login_required
@permission_required(['vaga.add_vaga'], login_url='lista-vagas')
def cadastrar_vaga(request: HttpRequest):
    endereco_ong = Ong.objects.filter(usuario=request.user).get().endereco
    if request.method == 'POST':
        form_vaga = VagaForm(request.POST)
        form_endereco = CadastroEnderecoForm(request.POST)

        if form_vaga.is_valid() and form_endereco.is_valid():
            endereco = form_endereco.save()
            vaga = form_vaga.save(commit=False)
            vaga.endereco = endereco
            vaga.ong = request.user.ong
            vaga.save()
            return redirect('minhas-vagas')
    else:
        form_vaga = VagaForm()
        form_endereco = CadastroEnderecoForm(instance=endereco_ong)
    return render(request, 'vaga/cadastro.html', {
        'form': form_vaga,
        'form_endereco': form_endereco
    })

class VagaList(ListView):
    model = Vaga
    template_name = 'vaga/vaga_list.html'

    def get_queryset(self):
        return Vaga.objects.filter(preenchida__exact=0, ong__status__exact='Ativa', fim_candidaturas__gte=datetime.datetime.now().date())

@login_required
@permission_required(['vaga.add_vaga'], login_url='lista-vagas')
def editar_vaga(request: HttpRequest, pk):
    if request.method == 'POST':
        form_vaga = VagaForm(request.POST)
        form_endereco = CadastroEnderecoForm(request.POST)

        if form_vaga.is_valid() and form_endereco.is_valid():
            endereco = form_endereco.save()
            vaga = form_vaga.save(commit=False)
            vaga.endereco = endereco
            vaga.ong = request.user.ong
            vaga.save()
            return redirect('minhas-vagas')
    else:
        vaga = Vaga.objects.filter(id=pk).first()
        endereco = Endereco.objects.filter(id=vaga.endereco.id).first()

        form_vaga = VagaForm(instance=vaga)
        form_endereco = CadastroEnderecoForm(instance=endereco)
    return render(request, 'vaga/vaga_edit.html', {
        'form': form_vaga,
        'form_endereco': form_endereco
    })

class VagaUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'vaga.change_vaga'
    model = Vaga
    form_class = EditarVagaForm
    template_name = 'vaga/vaga_edit.html'
    success_url = reverse_lazy('minhas-vagas')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['id_vaga'] = self.kwargs.get('pk')
        return kwargs

    def get_context_data(self, **kwargs):
        id_vaga = self.kwargs.get('pk')
        kwargs['id_vaga'] = id_vaga
        context = super(VagaUpdate, self).get_context_data(**kwargs)
        endereco_form = EditarEnderecoForm(self.request.POST or None, self.request.FILES or None, instance=Endereco.objects.get(id=self.get_object().endereco_id))
        if possui_candidatura(id_vaga):
            for campo in endereco_form.fields:
                endereco_form.fields[campo].disabled = True
        context['form_endereco'] = endereco_form
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        endereco_form = context['form_endereco']

        if form.is_valid() and endereco_form.is_valid():
            endereco = endereco_form.save()
            vaga = form.save(commit=False)
            vaga.endereco = endereco
            vaga.ong = self.request.user.ong
            vaga.save()
            return redirect('detalhe-vaga', vaga.id)
        else:
            return self.form_invalid(form)

class VagaDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'vaga.delete_vaga'
    model = Vaga
    template_name = 'vaga/vaga_delete.html'
    success_url = reverse_lazy('minhas-vagas')

class MinhasVagasList(PermissionRequiredMixin, VagaList):
    permission_required = 'vaga.visualizar_minhas_vagas'

    def get_queryset(self):
        ong = Ong.objects.filter(usuario_id__exact=self.request.user.id).get()
        return Vaga.objects.filter(ong_id__exact=ong.id)

@login_required
@permission_required(['vaga.change_vaga'], login_url='lista-vagas')
def preencher_vaga(request: HttpRequest, pk: int):
    if request.method == 'POST':
        try:
            Vaga.objects.filter(id=pk).update(preenchida=1)
        except Exception as e:
            messages.error(request, _('Erro ao preencher vaga, entre em contato com o administrador do sistema.'))
        else:
            messages.success(request, _('Vaga preenchida com sucesso!'))
        return redirect('detalhe-vaga', pk)
    return redirect('lista-vagas')