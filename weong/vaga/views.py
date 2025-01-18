from django.shortcuts import render
from django.views import generic
from vaga.models import Vaga

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
