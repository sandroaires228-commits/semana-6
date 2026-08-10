from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Servidor
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
