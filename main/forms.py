# main/forms.py
from django import forms
from .models import RegistroGasto

class RegistroGastoForm(forms.ModelForm):
    class Meta:
        model = RegistroGasto
        fields = ['descricao', 'valor', 'categoria', 'is_impulsivo']
        labels = {
            'descricao': 'Descrição da Compra',
            'valor': 'Valor (R$)',
            'categoria': 'Categoria do Gasto',
            'is_impulsivo': 'Marque se considerou esta compra impulsiva',
        }
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'campo-texto',
                'placeholder': 'Ex: Tênis esportivo, Lanche rápido, etc.'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'campo-numero',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'categoria': forms.Select(attrs={
                'class': 'campo-select'
            }),
            'is_impulsivo': forms.CheckboxInput(attrs={
                'class': 'campo-checkbox'
            }),
        }