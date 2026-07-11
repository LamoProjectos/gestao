from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('agenda/', views.agenda, name='agenda'),
    path('notificacoes/', views.notificacoes, name='notificacoes'),
    path('notificacoes/marcar-lidas/', views.marcar_lidas, name='marcar_lidas'),
]
