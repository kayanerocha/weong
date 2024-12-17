from django.contrib import admin
from vaga.models import Vaga

# Register your models here.

# admin.site.register(Vaga)

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'requisitos', 'local', 'preenchida')
    list_filter = ('titulo', 'local', 'preenchida')