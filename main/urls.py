from django.urls import path
from main import views

urlpatterns = [
    # Autenticação
    path('login/', views.fazer_login, name='login'),
    path('logout/', views.fazer_logout, name='logout'),
    path('registrar-operador/', views.registrar_operador, name='registrar_operador'),

    # Painel
    path('painel/', views.painel, name='painel'),

    # Ações de Gastos e Geladeira
    path('editar/<int:id>/', views.editar_gasto, name='editar_gasto'),
    path('excluir/<int:id>/', views.excluir, name='excluir'),
    path('geladeira/<int:id>/<str:acao>/', views.acao_geladeira, name='acao_geladeira'),
    path('meta/criar/', views.criar_meta, name='criar_meta'),

    # API
    path('api/gastos/', views.api_gastos, name='api_gastos'),
]