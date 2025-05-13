from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from usuario.models import Ong, Voluntario

# Register your models here.

class OngInline(admin.StackedInline):
    model = Ong
    can_delete = False
    verbose_name_plural = 'ongs'

@admin.register(Ong)
class OngAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'razao_social', 'cnpj', 'resumo', 'telefone', 'status')
    list_filter = ('status',)

class UserAdmin(BaseUserAdmin):
    inlines = [OngInline]

@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'telefone', 'data_nascimento', 'cpf', 'resumo', 'status')
    list_filter = ('status',)