from django.contrib import admin
from vaga.models import Vaga, Endereco

# Register your models here.

# admin.site.register(Vaga)

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'requisitos', 'endereco', 'preenchida', 'quantidade_vagas', 'fim_candidaturas', 'area')
    list_filter = ('preenchida', 'fim_candidaturas', 'area')

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_filter = ('bairro', 'cidade', 'estado')
