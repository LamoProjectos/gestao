from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nome', 'telefone', 'email', 'endereco', 'nuit', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'nuit': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email and Client.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Já existe um cliente com este email.')
        return email
