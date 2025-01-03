from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from usuario.models import Ong

# Register your models here.

class OngInline(admin.StackedInline):
    model = Ong
    can_delete = False
    verbose_name_plural = 'ongs'

@admin.register(Ong)
class OngAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'razao_social', 'cnpj', 'telefone', 'status')
    list_filter = ('nome_fantasia', 'status')

class UserAdmin(BaseUserAdmin):
    inlines = [OngInline]