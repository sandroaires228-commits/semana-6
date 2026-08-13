from django.contrib import admin
from django.urls import path
from main.views import painel_financeiro

urlpatterns = [
    path('admin/', admin.site.urls),
    # Rota para acessar o painel financeiro no navegador
    path('painel/', painel_financeiro, name='painel_financeiro'),
]