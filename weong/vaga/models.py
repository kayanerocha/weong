from django.db import models
from django.urls import reverse

# Create your models here.

class Endereco(models.Model):
    '''Modelo representando um endereco'''
    id = models.AutoField(primary_key=True)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255, null=True)
    cidade = models.CharField(max_length=255)

    ESTADOS = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    )

    estado = models.CharField(max_length=2, choices=ESTADOS)
    cep = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'endereco'

    def __str__(self):
        return f'{self.logradouro}, {self.numero}, {self.complemento} - {self.bairro}, {self.cidade} - {self.estado}, {self.cep}'.replace('- None', '').replace(', None', '')
    
    def get_absolute_url(self):
        return reverse('detalhe-endereco', args=[str(self.id)])

class Vaga(models.Model):
    '''Modelo representando uma vaga'''
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, help_text='Título da vaga')
    descricao = models.TextField(max_length=5000, help_text='Descrição da vaga')
    requisitos = models.TextField(max_length=2500, help_text='Requisitos da vaga')
    preenchida = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'vaga'

    def __str__(self):
        '''String representando um objeto'''
        return self.titulo
    
    def get_absolute_url(self):
        '''Retorna a URL para acessar detalhes de uma vaga'''
        return reverse('detalhe-vaga', args=[str(self.id)])
    