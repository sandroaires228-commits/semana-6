from django.urls import path
from main import views

urlpatterns = [
    # Dashboard
    path('painel/', views.painel, name='painel'),
    
    # Atualização, Exclusão e Ações
    path('editar/<int:id>/', views.editar_gasto, name='editar_gasto'),
    path('abortar/<int:id>/', views.abortar, name='abortar'),
    path('excluir/<int:id>/', views.excluir, name='excluir'),
    
    # Autenticação e Operador
    path('registrar-operador/', views.registrar_operador, name='registrar_operador'),
    path('logout/', views.fazer_logout, name='logout'),
    
    # API REST
    path('api/gastos/', views.api_gastos, name='api_gastos'),
]