from django import forms
from crm.models import Client
from .models import Project, ProjectStage
from .models import TIPO_PROJETO, STATUS_PROJETO


class ProjectForm(forms.ModelForm):
    importar_etapas = forms.BooleanField(
        required=False,
        label='Importar etapas padrão para este tipo de projeto',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Project
        fields = ['cliente', 'nome', 'tipo', 'status', 'descricao', 'valor_total', 'data_inicio', 'data_entrega']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Client.objects.all()

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get('data_inicio')
        entrega = cleaned.get('data_entrega')
        if inicio and entrega and entrega < inicio:
            raise forms.ValidationError('A data de entrega não pode ser anterior à data de início.')
        return cleaned


class ProjectStageForm(forms.ModelForm):
    class Meta:
        model = ProjectStage
        fields = ['ordem', 'nome', 'descricao', 'data_prevista']
        widgets = {
            'ordem': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'data_prevista': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
