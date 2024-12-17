from django.shortcuts import render
from vaga.models import Vaga

# Create your views here.

def index(request):
    '''View para a página home com listagem de vagas'''
    vagas = Vaga.objects.filter(preenchida__exact=0)

    context = {
        'vagas': vagas
    }

    return render(request, 'index.html', context=context)
