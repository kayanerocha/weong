from django.contrib import admin
from vaga.models import Vaga, Endereco

# Register your models here.

# admin.site.register(Vaga)

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'requisitos', 'endereco', 'preenchida')
    list_filter = ('titulo', 'preenchida')

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_filter = ('bairro', 'cidade', 'estado')
