from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('agenda/', views.agenda, name='agenda'),
    path('notificacoes/', views.notificacoes, name='notificacoes'),
    path('notificacoes/marcar-lidas/', views.marcar_lidas, name='marcar_lidas'),
    path('tarefas/', views.lista_tarefas, name='lista_tarefas'),
    path('tarefas/nova/', views.nova_tarefa, name='nova_tarefa'),
    path('tarefas/<int:pk>/editar/', views.editar_tarefa, name='editar_tarefa'),
    path('tarefas/<int:pk>/excluir/', views.excluir_tarefa, name='excluir_tarefa'),
    path('tarefas/<int:pk>/alternar/', views.alternar_tarefa, name='alternar_tarefa'),
    path('manifest.json', views.manifest, name='manifest'),
]
