from django.db import models

class RegistroGasto(models.Model):
    CATEGORIAS = [
        ('alimentacao', 'Alimentação'),
        ('eletronicos', 'Eletrônicos'),
        ('vestuario', 'Vestuário'),
        ('lazer', 'Lazer'),
        ('outros', 'Outros'),
    ]

    ESTADOS = [
        ('CONGELADO', 'Congelado na Geladeira'),
        ('PLANEJADO', 'Gasto Planejado'),
        ('DESISTIDO', 'Compra Abortada'),
    ]

    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='outros')
    impulso = models.BooleanField(default=False)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='PLANEJADO')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"