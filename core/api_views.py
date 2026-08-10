from rest_framework import viewsets

from .models import Servidor
from .serializers import ServidorSerializer


class ServidorViewSet(viewsets.ModelViewSet):
    queryset = Servidor.objects.all().order_by("hostname")
    serializer_class = ServidorSerializer
