from django import forms
from .models import Tarefa


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'data', 'prioridade', 'projeto', 'concluida']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'projeto': forms.Select(attrs={'class': 'form-select'}),
            'concluida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo'].strip()
        if len(titulo) < 3:
            raise forms.ValidationError('O título deve ter pelo menos 3 caracteres.')
        return titulo
