from django.urls import path
from . import views

urlpatterns = [
    # Tela Principal / Dashboard (Carregamento HTML + Cadastro via POST)
    path('painel/', views.painel, name='painel'),
    
    # Rota de Edição/Atualização de Produtos e Valores
    path('editar/<int:id>/', views.editar_gasto, name='editar_gasto'),
    
    # Rotas de Ação da Geladeira e Exclusão
    path('abortar/<int:id>/', views.abortar, name='abortar'),
    path('excluir/<int:id>/', views.excluir, name='excluir'),
    
    # Endpoint JSON para a Engine de Sincronização em Tempo Real (REST Polling)
    path('api/gastos/', views.api_gastos, name='api_gastos'),
]