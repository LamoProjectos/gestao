from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cotacoes, name='financial_lista'),
    path('nova/', views.nova_cotacao, name='financial_nova'),
    path('<int:pk>/', views.detalhe_cotacao, name='financial_detalhe'),
    path('<int:pk>/editar/', views.editar_cotacao, name='financial_editar'),
    path('<int:pk>/excluir/', views.excluir_cotacao, name='financial_excluir'),
    path('<int:pk>/pagar/', views.registrar_pagamento, name='financial_pagar'),
    path('extrato/', views.extrato, name='financial_extrato'),
    path('caixa/', views.lista_caixa, name='financial_caixa_lista'),
    path('caixa/novo/', views.novo_movimento, name='financial_caixa_novo'),
    path('caixa/<int:pk>/editar/', views.editar_movimento, name='financial_caixa_editar'),
    path('caixa/<int:pk>/excluir/', views.excluir_movimento, name='financial_caixa_excluir'),
    path('caixa/extrato/', views.extrato_caixa, name='financial_caixa_extrato'),
    path('caixa/relatorio/', views.relatorio_caixa, name='financial_caixa_relatorio'),
    path('config/assinatura/', views.config_assinatura, name='financial_config_assinatura'),
]
