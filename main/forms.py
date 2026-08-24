from django import forms
from .models import RegistroGasto

class RegistroGastoForm(forms.ModelForm):
    class Meta:
        model = RegistroGasto
        fields = ['descricao', 'valor', 'categoria', 'impulso']
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'placeholder': 'Ex: Fone Bluetooth, Supermercado, Lanche...'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select bg-dark text-light border-secondary'
            }),
            'impulso': forms.CheckboxInput(attrs={
                'class': 'form-check-input bg-dark border-secondary',
                'id': 'checkImpulso'
            }),
        }