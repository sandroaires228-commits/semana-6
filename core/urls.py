from django.contrib import admin
from django.urls import path
from main.views import painel_view, api_gastos_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', painel_view, name='home'),
    path('painel/', painel_view, name='painel'),
    path('api/gastos/', api_gastos_view, name='api_gastos'),
]