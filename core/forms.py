from django import forms

from .models import Servidor


class ServidorForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = ["hostname", "endereco_ip", "is_ativo"]


class FinanceiroFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Data Início",
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Data Fim",
    )
