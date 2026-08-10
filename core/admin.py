from django.contrib import admin

from .models import Servidor


@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    """Configura a exibição do model Servidor no painel administrativo."""
    list_display = ("hostname", "endereco_ip", "is_ativo", "data_registro")
    search_fields = ("hostname", "endereco_ip")
    list_filter = ("is_ativo",)
    readonly_fields = ("data_registro",)
