from rest_framework import serializers

from .models import Servidor


class ServidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servidor
        fields = ["id", "hostname", "endereco_ip", "is_ativo", "data_registro"]
