from django.db import models
from django.urls import reverse

# Create your models here.

class Vaga(models.Model):
    '''Modelo representando uma vaga'''
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, help_text='Título da vaga')
    descricao = models.TextField(max_length=5000, help_text='Descrição da vaga')
    requisitos = models.TextField(max_length=2500, help_text='Requisitos da vaga')
    local = models.CharField(max_length=100, help_text='Endereço do trabalho')
    preenchida = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vaga'

    def __str__(self):
        '''String representando um objeto'''
        return self.titulo
    
    def get_absolute_url(self):
        '''Retorna a URL para acessar detalhes de uma vaga'''
        return reverse('detalhe-vaga', args=[str(self.id)])
    