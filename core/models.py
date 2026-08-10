from django.db import models


class Servidor(models.Model):
    """Representa um servidor monitorado pela plataforma.

    Esta entidade mapeia a estrutura física de um servidor no banco de
    dados relacional. Os campos refletem os principais atributos usados
    pelo domínio de monitoramento e garantem validações essenciais como
    unicidade de hostname e formato válido de endereço IP.
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
        """Retorna uma representação legível do servidor.

        Esse método é utilizado em interfaces administrativas e logs para
        identificar o servidor por hostname e endereço IP.
        """
        return f"{self.hostname} ({self.endereco_ip})"
