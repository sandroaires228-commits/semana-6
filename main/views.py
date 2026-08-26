from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import logout
from .models import Gasto

def painel(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria', 'Geral')
        impulso = request.POST.get('impulso') == 'on'

        Gasto.objects.create(
            descricao=descricao,
            valor=valor,
            categoria=categoria,
            impulso=impulso,
            estado='CONGELADO' if impulso else 'PLANEJADO'
        )
        return redirect('painel')

    gastos = Gasto.objects.all().order_by('-id')
    gastos_geladeira = Gasto.objects.filter(estado='CONGELADO') | Gasto.objects.filter(impulso=True)
    economia_potencial = sum(g.valor for g in gastos_geladeira)

    return render(request, 'main/painel.html', {
        'gastos': gastos,
        'economia_potencial': economia_potencial,
        'total_geladeira': gastos_geladeira.count()
    })

def editar_gasto(request, id):
    gasto = get_object_or_404(Gasto, id=id)
    if request.method == 'POST':
        gasto.descricao = request.POST.get('descricao')
        gasto.valor = request.POST.get('valor')
        gasto.categoria = request.POST.get('categoria')
        gasto.save()
        return redirect('painel')
    return redirect('painel')

def abortar(request, id):
    gasto = get_object_or_404(Gasto, id=id)
    gasto.estado = 'DESISTIDO'
    gasto.save()
    return redirect('painel')

def excluir(request, id):
    gasto = get_object_or_404(Gasto, id=id)
    gasto.delete()
    return redirect('painel')

def registrar_operador(request):
    return redirect('painel')

def fazer_logout(request):
    logout(request)
    return redirect('painel')

def api_gastos(request):
    gastos = Gasto.objects.all().order_by('-id')
    data = [
        {
            'id': g.id,
            'descricao': g.descricao,
            'valor': str(g.valor),
            'categoria': g.categoria,
            'estado': g.estado,
            'impulso': g.impulso,
        }
        for g in gastos
    ]
    return JsonResponse(data, safe=False)