from django.db import models

class Gasto(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100, default='Geral')
    impulso = models.BooleanField(default=False)
    estado = models.CharField(max_length=50, default='PLANEJADO')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"