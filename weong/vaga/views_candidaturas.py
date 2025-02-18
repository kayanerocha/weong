from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Candidatura, Vaga

class CandidaturaCreate(PermissionRequiredMixin, CreateView):
    model = Candidatura
    success_url = reverse_lazy('detalhe-vaga')
    login_url = '403.html'

    def form_valid(self, form):
        candidatura = Candidatura()
        candidatura.vaga = Vaga()

        # context = self.get_context_data()
        # endereco_form = context['endereco_form']
        # if endereco_form.is_valid():
        #     endereco = endereco_form.save()
        #     vaga = form.save(commit=False)
        #     vaga.endereco = endereco
        #     vaga.ong = self.request.user.ong
        #     vaga.save()
        #     return super().form_valid(form)
        # else:
        #     return self.form_invalid(form)
