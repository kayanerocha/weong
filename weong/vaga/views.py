from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .models import Vaga
from .forms import VagaForm
from usuario.forms import CadastroEnderecoForm
from usuario.models import Ong, Voluntario, Endereco
from .views_candidaturas import candidatura_existe

class ListaVagasView(generic.ListView):
    model = Vaga
    context_object_name = 'lista_vagas'

    def get_queryset(self):
        return Vaga.objects.filter(preenchida__exact=0)
    
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
        try:
            if self.request.user.is_authenticated:
                voluntario = Voluntario.objects.filter(usuario_id=self.request.user.id).get()
                if candidatura_existe(context['object'].id, voluntario.id):
                    messages.info(self.request, _('Candidatura já realizada.'))
                    context['is_candidato'] = True
        except Voluntario.DoesNotExist:
            pass
        return context

class VagaCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'vaga.add_vaga'
    model = Vaga
    form_class = VagaForm
    template_name = 'vaga/cadastro.html'
    success_url = reverse_lazy('minhas-vagas')
    login_url = '403.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['endereco_form'] = CadastroEnderecoForm(self.request.POST)
        else:
            context['endereco_form'] = CadastroEnderecoForm()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        endereco_form = context['endereco_form']
        if endereco_form.is_valid():
            endereco = endereco_form.save()
            vaga = form.save(commit=False)
            vaga.endereco = endereco
            vaga.ong = self.request.user.ong
            vaga.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class VagaList(ListView):
    model = Vaga
    template_name = 'vaga/vaga_list.html'

    def get_queryset(self):
        return Vaga.objects.filter(preenchida__exact=0)

class VagaUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'vaga.change_vaga'
    model = Vaga
    form_class = VagaForm
    template_name = 'vaga/vaga_update.html'
    success_url = reverse_lazy('minhas-vagas')

    def get_context_data(self, **kwargs):
        context = super(VagaUpdate, self).get_context_data(**kwargs)
        context['endereco_form'] = CadastroEnderecoForm(self.request.POST or None, self.request.FILES or None, instance=Endereco.objects.get(id=self.get_object().endereco_id))
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        endereco_form = context['endereco_form']

        if form.is_valid() and endereco_form.is_valid():
            endereco = endereco_form.save()
            vaga = form.save(commit=False)
            vaga.endereco = endereco
            vaga.ong = self.request.user.ong
            vaga.save()
            return super().form_valid(form)
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