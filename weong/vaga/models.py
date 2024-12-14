from django.db import models

# Create your models here.

class Vaga(models.Model):
    '''Modelo representando vaga'''
    id = models.AutoField(primary_key=True)
    