from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from vaga.models import Endereco

# Create your models here.

class Ong(models.Model):
    '''Modelo representando uma ONG'''
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=11, help_text='Contato de um responsável da ONG.')
    site = models.URLField(max_length=255, blank=True, null=True)

    STATUS_ONG = (
        ('Pendente', 'Pendente'),
        ('Em análise', 'Em análise'),
        ('Ativa', 'Ativa'),
        ('Inativa', 'Inativa'),
    )

    status = models.CharField(max_length=50, choices=STATUS_ONG, default='Pendente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)

    class Meta:
        db_table = 'ongs'
    
    def __str__(self):
        return self.nome_fantasia
    
    def get_absolute_url(self):
        return reverse('detalhe-ong', args=[str(self.id)])

