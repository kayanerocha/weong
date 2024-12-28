from django.contrib import admin

from usuario.models import Ong

# Register your models here.

@admin.register(Ong)
class OngAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'razao_social', 'cnpj', 'telefone', 'status')
    list_filter = ('nome_fantasia', 'status')