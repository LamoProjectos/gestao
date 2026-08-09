from django.contrib import admin
from .models import Quote, Payment, CashFlow, CompanySettings


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ['prestacao', 'valor', 'data_vencimento', 'data_pagamento', 'status', 'metodo']


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'projeto', 'valor_total', 'data_emissao', 'data_validade', 'status']
    list_filter = ['status', 'data_emissao']
    search_fields = ['numero', 'cliente__nome']
    inlines = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['cotacao', 'prestacao', 'valor', 'data_vencimento', 'data_pagamento', 'status', 'metodo']
    list_filter = ['status', 'metodo']
    search_fields = ['cotacao__numero']


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'categoria', 'valor', 'data', 'descricao', 'cliente', 'projeto', 'forma_pagamento']
    list_filter = ['tipo', 'categoria', 'forma_pagamento', 'data']
    search_fields = ['descricao', 'documento', 'cliente__nome']


@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ['nome_administrador', 'cargo', 'atualizado_em']
