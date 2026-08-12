from django.contrib import admin

from .models import Servidor


@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    """
    Configuração da interface administrativa para a entidade Servidor.
    """
    list_display = ('hostname', 'endereco_ip', 'is_ativo', 'data_registro')
    search_fields = ('hostname', 'endereco_ip')
    list_filter = ('is_ativo', 'data_registro')
    ordering = ('hostname',)
