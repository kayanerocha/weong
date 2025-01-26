from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .models import Vaga
from .forms import VagaForm
from usuario.forms import CadastroEnderecoForm
from usuario.models import Ong

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

def editar_vaga(request, pk=None):
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    vaga = Vaga.objects.get(id=pk)
    form_vaga = VagaForm(request.POST or None, instance=vaga)
    form_endereco = CadastroEnderecoForm(request.POST or None, instance=vaga.endereco)

    if request.user.id != vaga.ong.usuario_id:
        return redirect('index')
    
    if request.method == 'POST':
        print('post')
        if form_vaga.is_valid() and form_endereco.is_valid():
            print('válido')
            form_endereco.save()
            form_vaga.save()

            return redirect('detalhe-vaga', pk=vaga.pk)
    return render(request, 'vaga/vaga_edit.html', {'form_vaga': form_vaga, 'form_endereco': form_endereco})

class VagaCreate(CreateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'vaga/cadastro.html'
    success_url = reverse_lazy('minhas-vagas')

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

class VagaDelete(DeleteView):
    model = Vaga
    template_name = 'vaga/vaga_delete.html'
    success_url = reverse_lazy('minhas-vagas')

class MinhasVagasList(VagaList):
    def get_queryset(self):
        ong = Ong.objects.filter(usuario_id__exact=self.request.user.id).get()
        return Vaga.objects.filter(ong_id__exact=ong.id)