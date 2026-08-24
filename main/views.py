@login_required(login_url='/admin/login/?next=/painel/')
def painel_view(request):
    if request.method == 'POST':
        form = RegistroGastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.estado = 'CONGELADO' if gasto.impulso else 'PLANEJADO'
            gasto.dias_reflexao = getattr(gasto, 'dias_reflexao', 7) or 7  # Preenche o valor obrigatório
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