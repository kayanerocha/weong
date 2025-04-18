from decouple import config
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone
from opencage.geocoder import OpenCageGeocode

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
    latitude = models.FloatField(max_length=20, blank=True, null=True)
    longitude = models.FloatField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'enderecos'

    def __str__(self):
        return f'{self.logradouro}, {self.numero}, {self.complemento} - {self.bairro}, {self.cidade} - {self.estado}, {self.cep}'.replace('- None', '').replace(', None', '')
    
    def get_absolute_url(self):
        return reverse('detalhe-endereco', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        geocoder = OpenCageGeocode(config('GEOCODER_API_KEY'))
        result = geocoder.geocode(self.__str__())
        if result:
            self.latitude = result[0]['geometry']['lat']
            self.longitude = result[0]['geometry']['lng']
        super().save(*args, **kwargs)


class Vaga(models.Model):
    '''Modelo representando uma vaga'''
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, help_text='Título da vaga')
    descricao = models.TextField(max_length=5000, help_text='Descrição da vaga')
    requisitos = models.TextField(max_length=2500, help_text='Requisitos da vaga')
    preenchida = models.BooleanField(default=False)
    quantidade_vagas = models.IntegerField(default=1, help_text='Quantidade de vagas')
    fim_candidaturas = models.DateField(help_text='Encerramento das candidaturas', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)
    ong = models.ForeignKey('usuario.Ong', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'vagas'
        permissions = (('visualizar_minhas_vagas', 'ONG visualizar as suas vagas.'),)

    def __str__(self):
        '''String representando um objeto'''
        return self.titulo
    
    def get_absolute_url(self):
        '''Retorna a URL para acessar detalhes de uma vaga'''
        return reverse('detalhe-vaga', args=[str(self.id)])
    
    def delete(self, using = None):
        if self.endereco:
            self.endereco.delete()
        super(Vaga, self).delete(using)

class Candidatura(models.Model):
    '''Modelo representando uma candidatura.'''
    id = models.AutoField(primary_key=True)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, null=True)
    voluntario = models.ForeignKey('usuario.Voluntario', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    STATUS_CANDIDATURA = (
        ('Pendente', 'Pendente'),
        ('Aceito', 'Aceito'),
        ('Recusado', 'Recusado'),
    )

    status = models.CharField(max_length=50, choices=STATUS_CANDIDATURA, default='Pendente')

    class Meta:
        db_table = 'candidaturas'

    def __str__(self):
        '''String representando um objeto'''
        return f'{self.id} - {self.vaga.titulo}: {self.candidato.nome_completo}'
    
    def get_absolute_url(self):
        '''Retorna a URL para acessar detalhes de uma inscrição'''
        return reverse('detalhe-inscricao', args=[str(self.id)])