from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


from .models import Vaga, Candidatura
from usuario.models import Voluntario

def candidatura_existe(vaga_id: int, voluntario_id: int):
    candidatura = Candidatura.objects.filter(vaga_id=vaga_id, voluntario_id=voluntario_id).first()
    if candidatura:
        return True
    return False

def criar_candidatura(request: HttpRequest, pk: int):
    if request.method == 'POST':
        vaga = Vaga.objects.filter(id=pk).get()
        voluntario = Voluntario.objects.filter(usuario_id=request.user.id).get()
        candidatura = Candidatura(vaga=vaga.id,voluntario=voluntario.id)
        candidatura.save()

        messages.success(request, _('Candidatura realizada com sucesso!'))
        return redirect('detalhe-vaga', pk)