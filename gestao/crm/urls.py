from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_clientes, name='crm_lista'),
    path('novo/', views.novo_cliente, name='crm_novo'),
    path('<int:pk>/editar/', views.editar_cliente, name='crm_editar'),
    path('<int:pk>/excluir/', views.excluir_cliente, name='crm_excluir'),
]
