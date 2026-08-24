from django.db import models
from django.utils import timezone
from datetime import timedelta

class RegistroGasto(models.Model):
    CATEGORIA_CHOICES = [
        ('essenciais', 'Gastos Essenciais'),
        ('lazer', 'Lazer'),
        ('eletronicos', 'Eletrônicos'),
        ('vestuario', 'Vestuário'),
        ('outros', 'Outros'),
    ]

    ESTADO_CHOICES = [
        ('PLANEJADO', 'Planejado / Efetivado'),
        ('CONGELADO', 'Na Geladeira (Reflexão)'),
        ('DESISTIDO', 'Compra Abortada (Economizado)'),
    ]

    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='outros')
    
    # Flags da Engenharia Comportamental
    impulso = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PLANEJADO')
    data_criacao = models.DateTimeField(auto_now_add=True)
    dias_reflexao = models.IntegerField(default=3) # Período padrão de resfriamento

    def esta_pronto_para_decisao(self):
        """Regra de Negócio: Verifica se o tempo de geladeira expirou."""
        if not self.impulso or self.estado != 'CONGELADO':
            return True
        data_liberacao = self.data_criacao + timedelta(dias=self.dias_reflexao)
        return timezone.now() >= data_liberacao

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor} [{self.estado}]"