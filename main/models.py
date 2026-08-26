from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class PerfilFinanceiro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', null=True, blank=True)
    renda_mensal = models.DecimalField(max_digits=10, decimal_places=2, default=2800.00)
    valor_hora = models.DecimalField(max_digits=8, decimal_places=2, default=17.50)
    limite_orcamento = models.DecimalField(max_digits=10, decimal_places=2, default=2800.00)

    def __str__(self):
        return f"Perfil de {self.user.username if self.user else 'Convidado'}"


class Gasto(models.Model):
    CATEGORIAS = [
        ('Alimentação', 'Alimentação'),
        ('Eletrônicos', 'Eletrônicos'),
        ('Transporte', 'Transporte'),
        ('Lazer', 'Lazer'),
        ('Vestuário', 'Vestuário'),
        ('Outros', 'Outros'),
    ]

    PRIORIDADES = [
        ('ESSENCIAL', 'Essencial'),
        ('IMPORTANTE', 'Importante'),
        ('NAO_ESSENCIAL', 'Não Essencial'),
        ('IMPULSIVO', 'Impulsivo'),
    ]

    ESTADOS = [
        ('PLANEJADO', 'Planejado'),
        ('CONGELADO', 'Geladeira de Compras'),
        ('DESISTIDO', 'Compra Desistida'),
        ('COMPRADO', 'Comprado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='Outros')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADES, default='IMPORTANTE')
    
    impulso = models.BooleanField(default=False)
    dias_reflexao = models.IntegerField(default=7)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PLANEJADO')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def calcular_horas_trabalho(self, valor_hora):
        if valor_hora and valor_hora > 0:
            return round(self.valor / Decimal(valor_hora), 1)
        return 0

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"


class MetaFinanceira(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=150)
    valor_objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_acumulado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_limite = models.DateField(null=True, blank=True)

    @property
    def percentual_concluido(self):
        if self.valor_objetivo > 0:
            p = (self.valor_acumulado / self.valor_objetivo) * 100
            return min(round(p, 1), 100)
        return 0.0

    def __str__(self):
        return f"{self.nome} ({self.percentual_concluido}%)"