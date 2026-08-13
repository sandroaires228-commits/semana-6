from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def painel_financeiro(request: HttpRequest) -> HttpResponse:
    """
    Renderiza o painel visual de gastos e injeta dados dinâmicos via contexto.
    """
    # Dicionário de Contexto: As chaves viram as variáveis {{ ... }} no HTML
    contexto_dados = {
        "gasto_descricao": "Fone de Ouvido Bluetooth (Oferta Flash)",
        "gasto_valor": "199.90",
        "gasto_gatilho": "Anúncio em Rede Social (Instagram)"
    }

    # A função render junta a requisição, o arquivo HTML e o contexto de dados
    return render(request, "main/painel.html", contexto_dados)