from django.urls import path

from .views import servidores_list, servidores_create, servidores_edit

urlpatterns = [
    path("", servidores_list, name="servidores_list"),
    path("novo/", servidores_create, name="servidores_create"),
    path("<int:pk>/editar/", servidores_edit, name="servidores_edit"),
]
