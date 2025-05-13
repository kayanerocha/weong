from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from vaga.models import Endereco
from .services import enviar_resultado_analise

# Create your models here.

class Ong(models.Model):
    '''Modelo representando uma ONG'''
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=11, help_text='Contato de um responsável da ONG.')
    site = models.URLField(max_length=255, blank=True, null=True)
    resumo = models.TextField(max_length=5000, default=' ')

    STATUS_ONG = (
        ('Pendente', 'Pendente'),
        ('Em análise', 'Em análise'),
        ('Ativa', 'Ativa'),
        ('Inativa', 'Inativa'),
    )

    status = models.CharField(max_length=50, choices=STATUS_ONG, default='Pendente')
    status_cnpj = models.CharField(max_length=20, default='Não informado')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)

    class Meta:
        db_table = 'ongs'
    
    def __str__(self):
        return self.razao_social or ' '
    
    def get_absolute_url(self):
        return reverse('detalhe-ong', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_status_ong = Ong.objects.get(pk=self.pk).status
            if old_status_ong != 'Ativa' and self.status == 'Ativa' or old_status_ong != 'Inativa' and self.status == 'Inativa':
                enviar_resultado_analise(self.status, self.usuario.email)
        return super().save(**kwargs)

class Voluntario(models.Model):
    '''Modelo representando um Voluntário'''
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    resumo = models.TextField(max_length=5000, default='')
    
    STATUS_VOLUNTARIO = (
        ('Pendente', 'Pendente'),
        ('Em análise', 'Em análise'),
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    )

    status = models.CharField(max_length=50, choices=STATUS_VOLUNTARIO, default='Pendente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)

    class Meta:
        db_table = 'voluntarios'

    def __str__(self):
        return self.nome_completo

    def get_absolute_url(self):
        return reverse('detalhe-voluntario', args=[str(self.id)])

class Coordenador(models.Model):
    '''Modelo representando um coordenador de ONG.'''
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    ong = models.OneToOneField(Ong, on_delete=models.CASCADE)

    STATUS_COORDENADOR = (
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo')
    )

    status = models.CharField(max_length=20, choices=STATUS_COORDENADOR, default='Inativo')

    class Meta:
        db_table = 'coordenadores'
    
    def __str__(self):
        return self.nome_completo
    
    def get_absolute_url(self):
        return reverse('detalhe-coordenador', args=[str(self.id)])
