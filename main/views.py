# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import RegistroGasto
from .forms import RegistroGastoForm

# ─── 1. VISÕES PROTEGIDAS (MVT) ───

@login_required  # Dia 33: Proteção de Rota por Autenticação
def painel_financeiro(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegistroGastoForm(request.POST)
        if form.is_valid():
            gasto = form.save()
            if gasto.is_impulsivo:
                messages.warning(request, f"⚠️ Alerta Anti-Impulso: O gasto '{gasto.descricao}' foi registrado como compra por impulso!")
            else:
                messages.success(request, f"✅ Lançamento planejado '{gasto.descricao}' registrado com sucesso.")
            return redirect('painel')
        else:
            messages.error(request, "Falha na validação do lançamento. Verifique os erros apontados no formulário.")
    else:
        form = RegistroGastoForm()

    todos_os_gastos = RegistroGasto.objects.all().order_by('-id')
    contexto = {
        'form': form,
        'lista_gastos': todos_os_gastos,
        'total_registros': todos_os_gastos.count()
    }
    return render(request, 'main/painel.html', contexto)

@login_required  # Dia 35: Exclusão Segura em 2 Passos
def view_excluir_gasto(request: HttpRequest, pk: int) -> HttpResponse:
    gasto_objeto = get_object_or_404(RegistroGasto, id=pk)

    if request.method == 'POST':
        descricao_excluida = gasto_objeto.descricao
        gasto_objeto.delete()
        messages.success(request, f"Registro '{descricao_excluida}' removido com sucesso do banco de dados!")
        return redirect('painel')

    return render(request, "main/confirmar_exclusao.html", {'gasto_excluir': gasto_objeto})

@login_required  # Dia 34: Gestão e Cadastro de Operadores
def view_registrar_operador(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            novo_usuario = form.save()
            messages.success(request, f"Novo operador '{novo_usuario.username}' cadastrado com sucesso!")
            return redirect('painel')
    else:
        form = UserCreationForm()

    return render(request, "main/registro_operador.html", {'form_cadastro': form})

# ─── 2. ROTAS DE API REST (JSON COM UTF-8) ───

def api_lista_gastos(request: HttpRequest) -> JsonResponse:  # Dia 37: Coleção Geral
    gastos = RegistroGasto.objects.all().order_by('-id')
    dados_api = []
    for g in gastos:
        dados_api.append({
            "id": g.id,
            "descricao": g.descricao,
            "valor": float(g.valor),
            "categoria": g.categoria.nome if g.categoria else None,
            "is_impulsivo": g.is_impulsivo
        })
    return JsonResponse(dados_api, safe=False, json_dumps_params={'ensure_ascii': False})

def api_detalhe_gasto(request: HttpRequest, pk: int) -> JsonResponse:  # Dia 37: Registro Individual & Erro 404
    try:
        gasto = RegistroGasto.objects.get(id=pk)
        payload = {
            "id": gasto.id,
            "descricao": gasto.descricao,
            "valor": float(gasto.valor),
            "categoria": gasto.categoria.nome if gasto.categoria else None,
            "is_impulsivo": gasto.is_impulsivo,
            "data": gasto.data.isoformat()
        }
        return JsonResponse(payload, json_dumps_params={'ensure_ascii': False})
    except RegistroGasto.DoesNotExist:
        return JsonResponse(
            {"erro": f"Lançamento #{pk} não consta no banco de dados."}, 
            status=404, 
            json_dumps_params={'ensure_ascii': False}
        )