from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


from .models import Vaga, Candidatura
from usuario.models import Voluntario

def candidatura_existe(vaga_id: int, voluntario_id: int):
    candidatura = Candidatura.objects.filter(vaga_id=vaga_id, voluntario_id=voluntario_id).first()
    if candidatura:
        return True
    return False

@login_required
@permission_required(['vaga.add_candidatura'], login_url='lista-vagas')
def criar_candidatura(request: HttpRequest, pk: int):
    if request.method == 'POST':
        try:
            vaga = Vaga.objects.filter(id=pk).get()
            voluntario = Voluntario.objects.filter(usuario_id=request.user.id).get()
            candidatura = Candidatura(vaga_id=vaga.id,voluntario_id=voluntario.id)
            candidatura.save()
        except Exception as e:
            messages.error(request, _('Erro ao realizar candidatura, entre em contato com o admistrador do sistema.'))
            print(e)
        return redirect('detalhe-vaga', pk)
    return redirect('lista-vagas')

class MinhasCandidaturas(PermissionRequiredMixin, ListView):
    permission_required = 'vaga.view_candidatura'
    model = Candidatura
    template_name = 'candidatura/candidatura_list.html'
    success_url = reverse_lazy('minhas-candidaturas')
    login_url = '403.html'

    def get_queryset(self):
        try:
            voluntario = Voluntario.objects.filter(usuario_id=self.request.user.id).get()
            print('aqui 1')
        except Voluntario.DoesNotExist:
            self.template_name = '403.html'
            print('ta caindo aqui essa porra')
        else:
            print('aqui 2')
            return Candidatura.objects.filter(voluntario_id=voluntario.id)
        
@login_required
@permission_required(['vaga.delete_candidatura'], login_url='lista-vagas')
def cancelar_candidatura(request: HttpRequest, pk: int):
    if request.method == 'POST':
        try:
            Candidatura.objects.filter(id=pk).delete()
        except Exception as e:
            messages.error(request, _('Erro ao cancelar a candidatura, entre em contato com o admistrador do sistema.'))
            print(e)
        else:
            messages.success(request, _('Candidatura cancelada com sucesso!'))
        return redirect('minhas-candidaturas')
    return redirect('lista-vagas')