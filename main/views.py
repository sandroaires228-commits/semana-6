from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import RegistroGasto
from .forms import RegistroGastoForm

# 1. View Principal do Painel
def painel_view(request):
    if request.method == 'POST':
        form = RegistroGastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.estado = 'CONGELADO' if gasto.impulso else 'PLANEJADO'
            gasto.save()
            return redirect('painel')
    else:
        form = RegistroGastoForm()

    registros = RegistroGasto.objects.exclude(estado='DESISTIDO').order_by('-id')
    economia_potencial = RegistroGasto.objects.filter(estado='CONGELADO').aggregate(total=Sum('valor'))['total'] or 0.00
    itens_geladeira = RegistroGasto.objects.filter(estado='CONGELADO').count()

    context = {
        'form': form,
        'registros': registros,
        'economia_potencial': economia_potencial,
        'itens_geladeira': itens_geladeira,
    }
    return render(request, 'main/painel.html', context)

# 2. View para Excluir Registro
def excluir_gasto_view(request, id):
    gasto = get_object_or_404(RegistroGasto, id=id)
    gasto.delete()
    return redirect('painel')

# 3. View para Editar Registro
def editar_gasto_view(request, id):
    gasto = get_object_or_404(RegistroGasto, id=id)
    if request.method == 'POST':
        form = RegistroGastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect('painel')
    else:
        form = RegistroGastoForm(instance=gasto)
    return render(request, 'main/editar_gasto.html', {'form': form, 'gasto': gasto})

# 4. View para Abortar Compra por Impulso
def abortar_compra_view(request, id):
    gasto = get_object_or_404(RegistroGasto, id=id)
    gasto.estado = 'DESISTIDO'
    gasto.save()
    return redirect('painel')

# 5. View para Cadastrar Operadores (Resolve o ImportError)
def registrar_operador_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('painel')
    else:
        form = UserCreationForm()
    return render(request, 'main/registrar_operador.html', {'form': form})

# 6. Endpoint de API JSON (Semana 9)
def api_gastos_view(request):
    gastos = RegistroGasto.objects.all().values('id', 'descricao', 'valor', 'categoria', 'impulso', 'estado')
    return JsonResponse(list(gastos), safe=False)