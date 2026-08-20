# core/urls.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from main.views import (
    painel_financeiro,
    view_excluir_gasto,
    view_registrar_operador,
    api_lista_gastos,
    api_detalhe_gasto
)

urlpatterns = [
    # Redireciona a raiz "/" para "/painel/"
    path('', lambda request: redirect('painel')),

    path('admin/', admin.site.urls),
    path('painel/', painel_financeiro, name='painel'),
    path('excluir/<int:pk>/', view_excluir_gasto, name='excluir_gasto'),
    path('registrar-operador/', view_registrar_operador, name='registrar_operador'),

    # APIs REST
    path('api/gastos/', api_lista_gastos, name='api_lista_gastos'),
    path('api/gastos/<int:pk>/', api_detalhe_gasto, name='api_detalhe_gasto'),

    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]