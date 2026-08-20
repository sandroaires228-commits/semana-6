from django.contrib import admin
from ..main.models import Categoria, RegistroGasto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Interface gerencial para o teto orçamentário das categorias.
    """
    list_display = ('nome', 'limite_mensal')
    search_fields = ('nome',)
    ordering = ('nome',)


@admin.register(RegistroGasto)
class RegistroGastoAdmin(admin.ModelAdmin):
    """
    Painel de auditoria de compras para monitorar e conter o consumo impulsivo.
    """
    # Colunas exibidas na tabela principal de listagem
    list_display = ('descricao', 'valor', 'categoria', 'is_impulsivo', 'gatilho', 'data_compra')

    # Painel lateral de filtros rápidos para isolar comportamentos de compra
    list_filter = ('is_impulsivo', 'gatilho', 'categoria', 'data_compra')

    # Barra de busca por nome do item ou por nome da categoria vinculada
    search_fields = ('descricao', 'categoria__nome')

    # Ordenação padrão: transações mais recentes no topo
    ordering = ('-data_compra',)