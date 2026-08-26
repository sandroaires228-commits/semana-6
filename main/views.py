from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .models import Gasto, MetaFinanceira, PerfilFinanceiro

@csrf_exempt
def fazer_login(request):
    """
    Renderiza e processa a autenticação do operador no sistema sem bloqueio de CSRF.
    """
    if request.user.is_authenticated:
        return redirect('painel')

    if request.method == 'POST':
        username_req = request.POST.get('username')
        password_req = request.POST.get('password')

        user = authenticate(request, username=username_req, password=password_req)

        if user is not None:
            login(request, user)
            return redirect('painel')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')

    return render(request, 'main/login.html')

def fazer_logout(request):
    """
    Encerra a sessão do operador e redireciona para a tela de login.
    """
    logout(request)
    return redirect('login')

def painel(request):
    usuario_atual = request.user if request.user.is_authenticated else None

    if usuario_atual:
        perfil, _ = PerfilFinanceiro.objects.get_or_create(
            user=usuario_atual,
            defaults={'renda_mensal': 2800.00, 'valor_hora': 17.50, 'limite_orcamento': 2800.00}
        )
    else:
        perfil = PerfilFinanceiro.objects.filter(user=None).first()
        if not perfil:
            perfil = PerfilFinanceiro.objects.create(
                user=None,
                renda_mensal=2800.00,
                valor_hora=17.50,
                limite_orcamento=2800.00
            )

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = Decimal(request.POST.get('valor', '0'))
        categoria = request.POST.get('categoria', 'Outros')
        prioridade = request.POST.get('prioridade', 'IMPORTANTE')
        impulso = request.POST.get('impulso') == 'on'

        estado = 'CONGELADO' if impulso or prioridade == 'IMPULSIVO' else 'PLANEJADO'

        Gasto.objects.create(
            user=usuario_atual,
            descricao=descricao,
            valor=valor,
            categoria=categoria,
            prioridade=prioridade,
            impulso=impulso,
            estado=estado
        )
        return redirect('painel')

    gastos = Gasto.objects.all().order_by('-data_criacao')
    gastos_efetivados = gastos.filter(estado__in=['PLANEJADO', 'COMPRADO'])
    gastos_geladeira = gastos.filter(estado='CONGELADO')
    gastos_desistidos = gastos.filter(estado='DESISTIDO')

    total_entradas = perfil.renda_mensal
    total_gastos = sum(g.valor for g in gastos_efetivados)
    saldo_disponivel = total_entradas - total_gastos
    economia_potencial = sum(g.valor for g in gastos_desistidos)
    economia_mes = economia_potencial + max(saldo_disponivel, Decimal(0))
    
    pct_orcamento = round((total_gastos / perfil.limite_orcamento) * 100, 1) if perfil.limite_orcamento > 0 else 0

    if pct_orcamento > 90 or gastos_geladeira.count() > 5:
        saude_financeira = {'status': 'Crítica', 'cor': '#EF4444', 'classe': 'text-danger', 'icone': '🔴'}
    elif pct_orcamento > 70 or gastos_geladeira.count() > 2:
        saude_financeira = {'status': 'Atenção', 'cor': '#F59E0B', 'classe': 'text-warning', 'icone': '🟡'}
    else:
        saude_financeira = {'status': 'Boa', 'cor': '#10B981', 'classe': 'text-success', 'icone': '🟢'}

    alertas = []
    if pct_orcamento >= 80:
        alertas.append(f"Você já utilizou {pct_orcamento}% do seu orçamento mensal.")
    if gastos_geladeira.count() > 0:
        alertas.append(f"Você possui {gastos_geladeira.count()} item(ns) sob reflexão na Geladeira.")
    if economia_potencial > 0:
        alertas.append(f"Você já evitou R$ {economia_potencial:.2f} em compras impulsivas este mês!")

    metas = MetaFinanceira.objects.all()

    return render(request, 'main/painel.html', {
        'gastos': gastos,
        'gastos_geladeira': gastos_geladeira,
        'metas': metas,
        'perfil': perfil,
        'total_entradas': total_entradas,
        'total_gastos': total_gastos,
        'saldo_disponivel': saldo_disponivel,
        'economia_potencial': economia_potencial,
        'economia_mes': economia_mes,
        'pct_orcamento': pct_orcamento,
        'saude_financeira': saude_financeira,
        'alertas': alertas,
    })

def acao_geladeira(request, id, acao):
    gasto = get_object_or_404(Gasto, id=id)
    if acao == 'comprar':
        gasto.estado = 'COMPRADO'
    elif acao == 'desistir':
        gasto.estado = 'DESISTIDO'
    gasto.save()
    return redirect('painel')

def criar_meta(request):
    if request.method == 'POST':
        MetaFinanceira.objects.create(
            user=request.user if request.user.is_authenticated else None,
            nome=request.POST.get('nome'),
            valor_objetivo=request.POST.get('valor_objetivo'),
            valor_acumulado=request.POST.get('valor_acumulado', 0)
        )
    return redirect('painel')

def editar_gasto(request, id):
    gasto = get_object_or_404(Gasto, id=id)
    if request.method == 'POST':
        gasto.descricao = request.POST.get('descricao')
        gasto.valor = request.POST.get('valor')
        gasto.categoria = request.POST.get('categoria')
        gasto.prioridade = request.POST.get('prioridade')
        gasto.save()
    return redirect('painel')

def excluir(request, id):
    gasto = get_object_or_404(Gasto, id=id)
    gasto.delete()
    return redirect('painel')

@csrf_exempt
def registrar_operador(request):
    """
    Cadastra um novo operador e o autentica diretamente no sistema.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        password = request.POST.get('password')

        if username and password:
            if not User.objects.filter(username=username).exists():
                novo_usuario = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password
                )
                login(request, novo_usuario)
                return redirect('painel')
    return redirect('login')

def api_gastos(request):
    gastos = Gasto.objects.all().order_by('-data_criacao')
    perfil = PerfilFinanceiro.objects.first()
    v_hora = perfil.valor_hora if perfil else Decimal(17.50)

    data = [
        {
            'id': g.id,
            'descricao': g.descricao,
            'valor': float(g.valor),
            'categoria': g.categoria,
            'prioridade': g.prioridade,
            'estado': g.estado,
            'horas_trabalho': g.calcular_horas_trabalho(v_hora),
            'data': g.data_criacao.strftime('%d/%m/%Y'),
        }
        for g in gastos
    ]
    return JsonResponse(data, safe=False)