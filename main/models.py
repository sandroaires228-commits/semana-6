from django.db import models


class Categoria(models.Model):
    """
    Representa o agrupamento temático de gastos (ex: Lazer, Alimentação, Eletrônicos).
    """
    nome = models.CharField(max_length=50, unique=True, verbose_name="Categoria")
    limite_mensal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Teto Orçamentário (R$)"
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self) -> str:
        return self.nome


class RegistroGasto(models.Model):
    """
    Mapeia as transações financeiras e audita os gatilhos de consumo impulsivo.
    """
    GATILHO_CHOICES = [
        ('REDE_SOCIAL', 'Anúncio em Rede Social'),
        ('E-MAIL_PROMOCIONAL', 'E-mail / Notificação de Promoção'),
        ('DESCONTO_TEMPORAL', 'Oferta por Tempo Limitado (Cupom/Flash Sale)'),
        ('NECESSIDADE_REAL', 'Compra Planejada / Necessidade Real'),
    ]

    descricao = models.CharField(max_length=100, verbose_name="Descrição do Item/Serviço")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor (R$)")
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="gastos", verbose_name="Categoria"
    )
    is_impulsivo = models.BooleanField(
        default=False, 
        verbose_name="Compra Impulsiva?", 
        help_text="Marque se a compra foi realizada sem planejamento prévio de 24 horas."
    )
    gatilho = models.CharField(
        max_length=30, 
        choices=GATILHO_CHOICES, 
        default='NECESSIDADE_REAL', 
        verbose_name="Gatilho de Consumo"
    )
    data_compra = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora da Transação")

    class Meta:
        verbose_name = "Registro de Gasto"
        verbose_name_plural = "Registros de Gastos"

    def __str__(self) -> str:
        tag_impulso = "[IMPULSIVO]" if self.is_impulsivo else "[PLANEJADO]"
        return f"{tag_impulso} {self.descricao} - R$ {self.valor}"