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
