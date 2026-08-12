from decimal import Decimal
from typing import Any

from django.db import models


class Servidor(models.Model):
    """Representa um servidor monitorado pela plataforma.

    Mantido para compatibilidade com as funcionalidades de monitoramento.
    """

    hostname: models.CharField = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nome da Máquina",
        help_text="Identificador único do servidor na rede.",
    )
    endereco_ip: models.GenericIPAddressField = models.GenericIPAddressField(
        protocol="both",
        verbose_name="Endereço IP",
        help_text="Endereço IPv4 ou IPv6 do servidor.",
    )
    is_ativo: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Monitoramento Ativo",
        help_text="Indica se o servidor está ativo para monitoramento.",
    )
    data_registro: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registro",
        help_text="Data e hora em que o servidor foi registrado.",
    )

    def __str__(self) -> str:
        return f"{self.hostname} ({self.endereco_ip})"


class Categoria(models.Model):
    """Categoria financeira que classifica lançamentos como Ativo ou Passivo.

    Tipos:
    - ATIVO: gera renda / ativo
    - PASSIVO: despesa / passivo
    """

    TIPO_ATIVO = "ATIVO"
    TIPO_PASSIVO = "PASSIVO"

    TIPO_CHOICES = [
        (TIPO_ATIVO, "Gerador de Renda/Ativo"),
        (TIPO_PASSIVO, "Despesa/Passivo"),
    ]

    nome: models.CharField = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nome da Categoria",
    )
    tipo: models.CharField = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default=TIPO_PASSIVO,
        verbose_name="Tipo",
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ("nome",)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.nome} ({self.tipo})"


class LancamentoFinanceiro(models.Model):
    """Registrar entradas financeiras (despesas e ativos).

    Modela lançamentos com vínculo a uma `Categoria` e fornece utilitários
    para avaliar se o lançamento é um ativo gerador de renda.
    """

    descricao: models.CharField = models.CharField(
        max_length=100,
        verbose_name="Descrição da Operação",
    )
    valor: models.DecimalField = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Valor (R$)",
    )
    categoria: models.ForeignKey = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        verbose_name="Categoria",
        related_name="lancamentos",
    )
    is_pago: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name="Liquidado / Pago",
    )
    data_vencimento: models.DateField = models.DateField(
        verbose_name="Data de Vencimento",
    )
    data_registro: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registro",
    )

    class Meta:
        verbose_name = "Lançamento Financeiro"
        verbose_name_plural = "Lançamentos Financeiros"
        ordering = ("-data_vencimento",)

    def is_ativo(self) -> bool:
        """Retorna True se a categoria do lançamento for do tipo 'ATIVO'."""
        return getattr(self.categoria, "tipo", None) == Categoria.TIPO_ATIVO

    def valor_normalizado(self) -> Decimal:
        """Retorna o valor como Decimal normalizado (útil para cálculos)."""
        return Decimal(self.valor)

    def __str__(self) -> str:
        status = "Pago" if self.is_pago else "Pendente"
        return f"{self.descricao} - R$ {self.valor} ({status})"
