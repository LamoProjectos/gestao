from django import forms
from datetime import date, timedelta
from crm.models import Client
from projects.models import Project
from .models import Quote, Payment, CashFlow, CompanySettings


class QuoteForm(forms.ModelForm):
    percentual_1 = forms.DecimalField(
        label='% 1ª Prestação', required=False, initial=50,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_p1', 'oninput': 'calcularPrestacoes()'}),
    )
    percentual_2 = forms.DecimalField(
        label='% 2ª Prestação', required=False, initial=50,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_p2', 'oninput': 'calcularPrestacoes()'}),
    )
    data_venc_1 = forms.DateField(
        label='Data Vencimento 1ª Prestação', required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    data_venc_2 = forms.DateField(
        label='Data Vencimento 2ª Prestação', required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

    class Meta:
        model = Quote
        fields = ['cliente', 'projeto', 'valor_total', 'data_validade', 'status', 'observacoes']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'projeto': forms.Select(attrs={'class': 'form-select'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'id_valor_total'}),
            'data_validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_validade'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Client.objects.all()
        self.fields['projeto'].queryset = Project.objects.all()
        self.fields['status'].required = False
        if not self.instance.pk and not self.initial.get('data_validade'):
            self.initial['data_validade'] = date.today() + timedelta(days=7)

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('percentual_1') or 0
        p2 = cleaned.get('percentual_2') or 0
        if p1 + p2 != 100:
            raise forms.ValidationError('A soma dos percentuais das prestações deve ser 100%.')
        return cleaned


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['data_pagamento', 'metodo', 'observacoes']
        widgets = {
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'metodo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transferência, M-Pesa, dinheiro...'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ['tipo', 'categoria', 'valor', 'data', 'descricao', 'cliente', 'cotacao', 'projeto',
                  'forma_pagamento', 'documento']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select', 'required': True, 'id': 'id_tipo', 'onchange': 'toggleCategorias()'}),
            'categoria': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'cotacao': forms.Select(attrs={'class': 'form-select'}),
            'projeto': forms.Select(attrs={'class': 'form-select'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-select'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Client.objects.all()
        self.fields['cotacao'].queryset = Quote.objects.all()
        self.fields['projeto'].queryset = Project.objects.all()

    def clean_valor(self):
        valor = self.cleaned_data['valor']
        if valor <= 0:
            raise forms.ValidationError('O valor deve ser maior que zero.')
        return valor


class CompanySettingsForm(forms.ModelForm):
    class Meta:
        model = CompanySettings
        fields = ['assinatura', 'nome_administrador', 'cargo']
        widgets = {
            'assinatura': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nome_administrador': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
        }
