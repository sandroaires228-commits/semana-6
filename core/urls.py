from django.urls import path

from .views import servidores_list, servidores_create, servidores_edit
from rest_framework import routers
from .api_views import ServidorViewSet

router = routers.DefaultRouter()
router.register(r"api/servidores", ServidorViewSet, basename="servidor")

urlpatterns = [
    path("", servidores_list, name="servidores_list"),
    path("novo/", servidores_create, name="servidores_create"),
    path("<int:pk>/editar/", servidores_edit, name="servidores_edit"),
]

urlpatterns += router.urls
