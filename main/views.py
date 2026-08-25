import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import RegistroGasto
from .forms import RegistroGastoForm


@login_required(login_url='/admin/login/?next=/painel/')
def painel_view(request):
    """View principal do painel financeiro DOMINUS SYS."""
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


def registrar_operador_view(request):
    """View para cadastro de novos operadores/usuários no sistema."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('painel')
    else:
        form = UserCreationForm()
    return render(request, 'main/registro_operador.html', {'form': form})


@csrf_exempt
def api_gastos_view(request):
    """Endpoint API REST da Semana 9 para consumo/envio em JSON."""
    if request.method == 'GET':
        gastos = RegistroGasto.objects.all().values('id', 'descricao', 'valor', 'categoria', 'impulso', 'estado')
        return JsonResponse(list(gastos), safe=False)

    elif request.method == 'POST':
        try:
            dados = json.loads(request.body)
            novo_gasto = RegistroGasto.objects.create(
                descricao=dados.get('descricao'),
                valor=dados.get('valor'),
                categoria=dados.get('categoria', 'outros'),
                impulso=dados.get('impulso', False),
                estado='CONGELADO' if dados.get('impulso') else 'PLANEJADO'
            )
            return JsonResponse({'mensagem': 'Registro criado com sucesso via API!', 'id': novo_gasto.id}, status=201)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)