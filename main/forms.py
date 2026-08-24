from django import forms
from .models import RegistroGasto

class RegistroGastoForm(forms.ModelForm):
    class Meta:
        model = RegistroGasto
        fields = ['descricao', 'valor', 'categoria', 'impulso']
        
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary shadow-none',
                'placeholder': 'Ex: Fone Bluetooth, Supermercado, Lanche...',
                'required': 'required',
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary shadow-none',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
                'required': 'required',
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select bg-dark text-white border-secondary shadow-none',
                'required': 'required',
            }),
            'impulso': forms.CheckboxInput(attrs={
                'class': 'form-check-input bg-dark border-danger',
                'style': 'cursor: pointer; width: 1.3em; height: 1.3em;',
                'id': 'checkImpulso'
            }),
        }

    # Validação personalizada para barrar valores menores ou iguais a zero
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise forms.ValidationError("O valor do lançamento deve ser maior que R$ 0,00.")
        return valor