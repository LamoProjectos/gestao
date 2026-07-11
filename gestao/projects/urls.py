from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_projetos, name='projects_lista'),
    path('novo/', views.novo_projeto, name='projects_novo'),
    path('<int:pk>/', views.detalhe_projeto, name='projects_detalhe'),
    path('<int:pk>/editar/', views.editar_projeto, name='projects_editar'),
    path('<int:pk>/excluir/', views.excluir_projeto, name='projects_excluir'),
    path('<int:pk>/etapa/nova/', views.nova_etapa, name='projects_nova_etapa'),
    path('etapa/<int:pk>/excluir/', views.excluir_etapa, name='projects_excluir_etapa'),
]
