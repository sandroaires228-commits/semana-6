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

    def get_tipo_financeiro(self, obj: LancamentoFinanceiro) -> str:
        """Retorna 'Ativo' ou 'Passivo' dependendo da categoria."""
        return 'Ativo' if obj.is_ativo() else 'Passivo'

    get_tipo_financeiro.short_description = 'Tipo Financeiro'
