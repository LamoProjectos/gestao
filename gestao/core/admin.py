from django.contrib import admin
from .models import Notification, AgendaEvent, Tarefa

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


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data', 'prioridade', 'projeto', 'concluida', 'atrasada']
    list_filter = ['prioridade', 'concluida', 'data']
    search_fields = ['titulo', 'descricao']
    ordering = ['-data']
