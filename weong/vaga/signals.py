from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Candidatura, Vaga
from .views import candidatos_selecionados

@receiver(post_save, sender=Candidatura)
def atualizar_preenchida(sender, instance, **kwargs):
    if not candidatos_selecionados(instance.vaga_id):
        Vaga.objects.filter(id=instance.vaga_id).update(preenchida=0)