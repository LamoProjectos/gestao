from django.urls import path
from . import views

urlpatterns = [
    path('cotacao/<int:pk>/pdf/', views.gerar_cotacao_pdf, name='doc_cotacao_pdf'),
    path('recibo/<int:pk>/pdf/', views.gerar_recibo_pdf, name='doc_recibo_pdf'),
    path('contrato/<int:pk>/pdf/', views.gerar_contrato_pdf, name='doc_contrato_pdf'),
]
