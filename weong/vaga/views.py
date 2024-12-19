from django.shortcuts import render
from django.views import generic
from vaga.models import Vaga

# Create your views here.

def index(request):
    '''View para a página home com listagem de vagas'''
    vagas = Vaga.objects.filter(preenchida__exact=0)

    context = {
        'titulo': 'Vagas Abertas',
        'vagas': vagas
    }

    return render(request, 'index.html', context=context)

class DetalheVagaView(generic.DetailView):
    model = Vaga
