from django.contrib import admin

from .models import Servidor


@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    """
    Configuração da interface administrativa para a entidade Servidor.
    """
    # Colunas exibidas na tabela de listagem
    list_display = ('hostname', 'endereco_ip', 'is_ativo', 'data_registro')

    # Barra de busca por nome da máquina ou por endereço IP
    search_fields = ('hostname', 'endereco_ip')

    # Filtros laterais categóricos e temporais
    list_filter = ('is_ativo', 'data_registro')

    # Ordenação padrão alfabética pelo hostname
    ordering = ('hostname',)


# Registros administrativos financeiros
from .models import Categoria, LancamentoFinanceiro
from django import forms
from django.utils import timezone


class LancamentoFinanceiroAdminForm(forms.ModelForm):
    class Meta:
        model = LancamentoFinanceiro
        fields = '__all__'

    def clean_valor(self):
        v = self.cleaned_data.get('valor')
        if v is None:
            return v
        if v <= 0:
            raise forms.ValidationError('O valor deve ser maior que zero.')
        return v

    def clean(self):
        cleaned = super().clean()
        data_venc = cleaned.get('data_vencimento')
        is_pago = cleaned.get('is_pago')
        if data_venc and is_pago and data_venc > timezone.localdate():
            # permitir, mas emitir aviso como ValidationError para forçar confirmação
            raise forms.ValidationError('Não é recomendado marcar como pago antes da data de vencimento.')
        return cleaned


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin para categorias financeiras."""
    list_display = ('nome', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nome',)


@admin.register(LancamentoFinanceiro)
class LancamentoFinanceiroAdmin(admin.ModelAdmin):
    """Admin para lançamentos financeiros com visão executiva."""
    list_display = (
        'descricao',
        'valor',
        'categoria',
        'get_tipo_financeiro',
        'is_pago',
        'data_vencimento',
        'data_registro',
    )
    list_filter = ('is_pago', 'categoria__tipo', 'data_vencimento')
    search_fields = ('descricao', 'categoria__nome')
    ordering = ('-data_vencimento',)
    form = LancamentoFinanceiroAdminForm
    list_editable = ('is_pago',)
    readonly_fields = ('data_registro',)
    fieldsets = (
        (None, {
            'fields': ('descricao', 'valor', 'categoria')
        }),
        ('Status', {
            'fields': ('is_pago', 'data_vencimento', 'data_registro')
        }),
    )

    actions = ('mark_as_paid', 'mark_as_unpaid')

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(is_pago=True)
        self.message_user(request, f'{updated} lançamentos marcados como pagos.')

    def mark_as_unpaid(self, request, queryset):
        updated = queryset.update(is_pago=False)
        self.message_user(request, f'{updated} lançamentos marcados como pendentes.')

    mark_as_paid.short_description = 'Marcar selecionados como pagos'
    mark_as_unpaid.short_description = 'Marcar selecionados como pendentes'

    def get_tipo_financeiro(self, obj: LancamentoFinanceiro) -> str:
        """Retorna 'Ativo' ou 'Passivo' dependendo da categoria."""
        return 'Ativo' if obj.is_ativo() else 'Passivo'

    get_tipo_financeiro.short_description = 'Tipo Financeiro'
