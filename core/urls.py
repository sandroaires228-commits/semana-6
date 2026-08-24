from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from main.views import (
    painel_view,
    excluir_gasto_view,
    editar_gasto_view,
    abortar_compra_view,
    registrar_operador_view,
    api_gastos_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', painel_view, name='home'),
    path('painel/', painel_view, name='painel'),
    path('excluir/<int:id>/', excluir_gasto_view, name='excluir_gasto'),
    path('editar/<int:id>/', editar_gasto_view, name='editar_gasto'),
    path('abortar/<int:id>/', abortar_compra_view, name='abortar_compra'),
    path('registrar-operador/', registrar_operador_view, name='registrar_operador'),
    path('api/gastos/', api_gastos_view, name='api_gastos'),
    path('logout/', auth_views.LogoutView.as_view(next_page='painel'), name='logout'),
]