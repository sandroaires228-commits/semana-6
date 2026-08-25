import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import RegistroGasto
from .forms import RegistroGastoForm

# ATENÇÃO PARA O NOME EXATO DA FUNÇÃO AQUI:
@login_required(login_url='/admin/login/?next=/painel/')
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

# ENDPOINT DA SEMANA 9
@csrf_exempt
def api_gastos_view(request):
    if request.method == 'GET':
        gastos = RegistroGasto.objects.all().values('id', 'descricao', 'valor', 'categoria', 'impulso', 'estado')
        return JsonResponse(list(gastos), safe=False)
    return JsonResponse({'erro': 'Método não permitido'}, status=405)