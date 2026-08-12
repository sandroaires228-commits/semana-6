from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import FinanceiroFilterForm
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.db.models.functions import TruncMonth

from .models import Servidor, Categoria, LancamentoFinanceiro
from .forms import ServidorForm


def servidores_list(request):
    q = request.GET.get("q", "").strip()
    servidores_qs = Servidor.objects.all()
    if q:
        servidores_qs = servidores_qs.filter(
            Q(hostname__icontains=q) | Q(endereco_ip__icontains=q)
        )
    servidores_qs = servidores_qs.order_by("hostname")

    paginator = Paginator(servidores_qs, 10)  # 10 por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "core/servidores_list.html",
        {"servidores": page_obj, "q": q},
    )


def servidores_create(request):
    if request.method == "POST":
        form = ServidorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("servidores_list")
    else:
        form = ServidorForm()
    return render(request, "core/servidor_form.html", {"form": form})


def servidores_edit(request, pk):
    servidor = get_object_or_404(Servidor, pk=pk)
    if request.method == "POST":
        form = ServidorForm(request.POST, instance=servidor)
        if form.is_valid():
            form.save()
            return redirect("servidores_list")
    else:
        form = ServidorForm(instance=servidor)
    return render(request, "core/servidor_form.html", {"form": form, "servidor": servidor})


@login_required
@staff_member_required
@permission_required('core.view_lancamentofinanceiro', raise_exception=True)
def financeiro_dashboard(request):
    """Dashboard executivo que sumariza Ativos x Passivos e por categoria.

    Exibe totais agregados e um resumo por categoria para auxiliar decisões
    financeiras rápidas (visão inspirada em conceitos de fluxo de caixa).
    """

    form = FinanceiroFilterForm(request.GET or None)

    qs = LancamentoFinanceiro.objects.all()
    if form.is_valid():
        start = form.cleaned_data.get("start_date")
        end = form.cleaned_data.get("end_date")
        if start and end:
            qs = qs.filter(data_vencimento__range=(start, end))
        elif start:
            qs = qs.filter(data_vencimento__gte=start)
        elif end:
            qs = qs.filter(data_vencimento__lte=end)

    total_ativos = (
        qs.filter(categoria__tipo=Categoria.TIPO_ATIVO)
        .aggregate(total=Sum("valor"))
        .get("total")
    )
    total_passivos = (
        qs.filter(categoria__tipo=Categoria.TIPO_PASSIVO)
        .aggregate(total=Sum("valor"))
        .get("total")
    )

    total_ativos = total_ativos or Decimal("0.00")
    total_passivos = total_passivos or Decimal("0.00")

    categorias = (
        Categoria.objects.all()
        .annotate(total=Sum("lancamentos__valor"))
        .order_by("-total")
    )

    context = {
        "total_ativos": total_ativos,
        "total_passivos": total_passivos,
        "categorias": categorias,
        "filter_form": form,
    }

    return render(request, "core/financeiro_dashboard.html", context)


@login_required
@staff_member_required
def financeiro_trends(request):
    """Retorna séries temporais agregadas (ativos/passivos) por mês em JSON.

    Aceita os mesmos parâmetros `start_date` e `end_date` do filtro do dashboard.
    """

    form = FinanceiroFilterForm(request.GET or None)
    qs = LancamentoFinanceiro.objects.all()
    if form.is_valid():
        start = form.cleaned_data.get("start_date")
        end = form.cleaned_data.get("end_date")
        if start and end:
            qs = qs.filter(data_vencimento__range=(start, end))
        elif start:
            qs = qs.filter(data_vencimento__gte=start)
        elif end:
            qs = qs.filter(data_vencimento__lte=end)

    # agrupa por mês e tipo de categoria
    qs_month = (
        qs.annotate(month=TruncMonth("data_vencimento"))
        .values("month", "categoria__tipo")
        .annotate(total=Sum("valor"))
        .order_by("month")
    )

    # montar dicionário por mês
    series = {}
    for row in qs_month:
        month = row["month"].strftime("%Y-%m")
        tipo = row["categoria__tipo"]
        total = float(row["total"] or 0)
        if month not in series:
            series[month] = {"ativo": 0.0, "passivo": 0.0}
        if tipo == Categoria.TIPO_ATIVO:
            series[month]["ativo"] += total
        else:
            series[month]["passivo"] += total

    labels = list(series.keys())
    ativos = [series[k]["ativo"] for k in labels]
    passivos = [series[k]["passivo"] for k in labels]

    return JsonResponse({"labels": labels, "ativos": ativos, "passivos": passivos})
