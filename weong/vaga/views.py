from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from django.utils.translation import gettext_lazy as _

from .models import Vaga
from .forms import VagaForm
from usuario.forms import CadastroEnderecoForm

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

def cadastro_vaga(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form_vaga = VagaForm(request.POST)
        form_endereco = CadastroEnderecoForm(request.POST)

        if form_vaga.is_valid() and form_endereco.is_valid():
            endereco = form_endereco.save()
            vaga = form_vaga.save(commit=False)
            vaga.endereco = endereco
            vaga.save()
            return redirect('detalhe-vaga', pk=vaga.pk)
        else:
            messages.error(request, _('Cadastro de vaga não realizado.'))
    else:
        form_vaga = VagaForm()
        form_endereco = CadastroEnderecoForm()

    return render(request, 'vaga/cadastro.html', {'form_vaga': form_vaga, 'form_endereco': form_endereco})