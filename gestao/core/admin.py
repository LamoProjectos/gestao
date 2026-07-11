from django.contrib import admin
from .models import Notification, AgendaEvent

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['mensagem', 'tipo', 'user', 'lida', 'criado_em']
    list_filter = ['tipo', 'lida', 'criado_em']
    search_fields = ['mensagem']

@admin.register(AgendaEvent)
class AgendaEventAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'data', 'projeto', 'concluido']
    list_filter = ['tipo', 'concluido', 'data']
    search_fields = ['titulo']
