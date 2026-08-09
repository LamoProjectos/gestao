from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'email', 'endereco', 'nuit', 'criado_em']
    search_fields = ['nome', 'telefone', 'email', 'nuit']
    list_filter = ['criado_em']
    ordering = ['-criado_em']
