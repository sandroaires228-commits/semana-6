from decimal import Decimal
from django import template

register = template.Library()


@register.filter()
def brl(value):
    """Formata um número como moeda brasileira (R$ 1.234,56).

    Aceita int, float ou Decimal. Retorna string formatada com prefixo R$.
    """
    try:
        d = Decimal(value)
    except Exception:
        return value

    # Formata com separador de milhar como vírgula e ponto decimal, ex: 1,234.56
    s = f"{d:,.2f}"
    # Converte para formato brasileiro: 1.234,56
    s = s.replace(
        ",", "_"
    ).replace(
        ".", ","
    ).replace(
        "_", "."
    )
    return f"R$ {s}"
