from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from crm.models import Client
from projects.models import Project
from .models import Quote, Payment, CashFlow, CompanySettings, CATEGORIAS_CAIXA, FORMA_PAGAMENTO
from .decorators import admin_required, add_user_context
from .forms import QuoteForm, PaymentForm, CashFlowForm, CompanySettingsForm


@login_required
def lista_cotacoes(request):
    cotacoes = Quote.objects.all()
    return render(request, 'financial/lista.html', add_user_context(request, {'cotacoes': cotacoes}))


@admin_required
def nova_cotacao(request):
    clientes = Client.objects.all()
    projetos = Project.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            valor_total = data['valor_total']
            valor_1 = round(valor_total * (data['percentual_1'] or 0) / 100, 2)
            valor_2 = round(valor_total * (data['percentual_2'] or 0) / 100, 2)

            ultimo_numero = Quote.objects.count() + 1
            ano = timezone.now().year
            numero = f'LP-{ano}-{ultimo_numero:03d}'

            cotacao = Quote.objects.create(
                cliente=data['cliente'], projeto=data['projeto'],
                numero=numero, valor_total=valor_total,
                valor_primeira_prestacao=valor_1,
                valor_segunda_prestacao=valor_2,
                data_validade=data['data_validade'],
                observacoes=data['observacoes']
            )

            data_venc_1 = data['data_venc_1'] or timezone.now().date()
            data_venc_2 = data['data_venc_2'] or timezone.now().date()
            Payment.objects.create(cotacao=cotacao, prestacao=1, valor=valor_1, data_vencimento=data_venc_1)
            Payment.objects.create(cotacao=cotacao, prestacao=2, valor=valor_2, data_vencimento=data_venc_2)

            messages.success(request, f'Cotação {numero} criada com sucesso!')
            return redirect('financial_detalhe', pk=cotacao.pk)
        messages.error(request, 'Corrija os erros do formulário.')
    else:
        form = QuoteForm()

    return render(request, 'financial/form.html', add_user_context(request, {
        'clientes': clientes, 'projetos': projetos, 'form': form, 'titulo': 'Nova Cotação'
    }))


@login_required
def detalhe_cotacao(request, pk):
    cotacao = get_object_or_404(Quote, pk=pk)
    pagamentos = cotacao.pagamentos.all()
    return render(request, 'financial/detalhe.html', add_user_context(request, {
        'cotacao': cotacao, 'pagamentos': pagamentos
    }))


@admin_required
def editar_cotacao(request, pk):
    cotacao = get_object_or_404(Quote, pk=pk)
    clientes = Client.objects.all()
    projetos = Project.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=cotacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cotação atualizada com sucesso!')
            return redirect('financial_detalhe', pk=cotacao.pk)
        messages.error(request, 'Corrija os erros do formulário.')
    else:
        form = QuoteForm(instance=cotacao)

    return render(request, 'financial/form.html', add_user_context(request, {
        'cotacao': cotacao, 'clientes': clientes, 'projetos': projetos,
        'form': form, 'titulo': 'Editar Cotação'
    }))


@admin_required
def excluir_cotacao(request, pk):
    cotacao = get_object_or_404(Quote, pk=pk)
    if request.method == 'POST':
        cotacao.delete()
        messages.success(request, 'Cotação excluída com sucesso!')
        return redirect('financial_lista')
    return render(request, 'financial/confirmar_exclusao.html', {'cotacao': cotacao, 'is_admin': True})


@admin_required
def registrar_pagamento(request, pk):
    pagamento = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=pagamento)
        if form.is_valid():
            pagamento = form.save(commit=False)
            if not pagamento.data_pagamento:
                pagamento.data_pagamento = timezone.now().date()
            pagamento.status = 'pago'
            pagamento.save()

            cotacao = pagamento.cotacao
            todos_pagos = all(p.status == 'pago' for p in cotacao.pagamentos.all())
            if todos_pagos:
                cotacao.status = 'aprovada'
                cotacao.save()

            messages.success(request, f'{pagamento.prestacao}ª Prestação registada como paga!')
            return redirect('financial_detalhe', pk=pagamento.cotacao.pk)
        messages.error(request, 'Corrija os erros do formulário.')

    form = PaymentForm(instance=pagamento)
    return render(request, 'financial/pagar.html', add_user_context(request, {
        'pagamento': pagamento, 'form': form, 'is_admin': True
    }))


@login_required
def extrato(request):
    pagamentos = Payment.objects.all().order_by('-data_pagamento')
    total_pendente = sum(p.valor for p in pagamentos if p.status == 'pendente')
    return render(request, 'financial/extrato.html', add_user_context(request, {
        'pagamentos': pagamentos, 'total_pendente': total_pendente
    }))


# ─── Caixa (Cash Flow) ─────────────────────────────────────────────

@login_required
def lista_caixa(request):
    movimentos = CashFlow.objects.all()
    saldo_entradas = sum(m.valor for m in movimentos if m.tipo == 'entrada')
    saldo_saidas = sum(m.valor for m in movimentos if m.tipo == 'saida')
    saldo = saldo_entradas - saldo_saidas

    tipo = request.GET.get('tipo', '')
    categoria = request.GET.get('categoria', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    if tipo:
        movimentos = movimentos.filter(tipo=tipo)
    if categoria:
        movimentos = movimentos.filter(categoria=categoria)
    if data_inicio:
        movimentos = movimentos.filter(data__gte=data_inicio)
    if data_fim:
        movimentos = movimentos.filter(data__lte=data_fim)

    return render(request, 'financial/caixa_lista.html', add_user_context(request, {
        'movimentos': movimentos,
        'saldo': saldo,
        'total_entradas': saldo_entradas,
        'total_saidas': saldo_saidas,
        'categorias_caixa': CATEGORIAS_CAIXA,
        'filtro_tipo': tipo,
        'filtro_categoria': categoria,
        'filtro_data_inicio': data_inicio,
        'filtro_data_fim': data_fim,
    }))


@admin_required
def novo_movimento(request):
    clientes = Client.objects.all()
    cotacoes = Quote.objects.all()
    projetos = Project.objects.all()
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimento registado com sucesso!')
            return redirect('financial_caixa_lista')
        messages.error(request, 'Corrija os erros do formulário.')
    else:
        form = CashFlowForm()

    return render(request, 'financial/caixa_form.html', add_user_context(request, {
        'clientes': clientes, 'cotacoes': cotacoes, 'projetos': projetos,
        'form': form, 'titulo': 'Novo Movimento',
        'categorias_caixa': CATEGORIAS_CAIXA, 'formas_pagamento': FORMA_PAGAMENTO,
    }))


@admin_required
def editar_movimento(request, pk):
    movimento = get_object_or_404(CashFlow, pk=pk)
    clientes = Client.objects.all()
    cotacoes = Quote.objects.all()
    projetos = Project.objects.all()
    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=movimento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimento atualizado com sucesso!')
            return redirect('financial_caixa_lista')
        messages.error(request, 'Corrija os erros do formulário.')
    else:
        form = CashFlowForm(instance=movimento)

    return render(request, 'financial/caixa_form.html', add_user_context(request, {
        'movimento': movimento, 'clientes': clientes, 'cotacoes': cotacoes, 'projetos': projetos,
        'form': form, 'titulo': 'Editar Movimento',
        'categorias_caixa': CATEGORIAS_CAIXA, 'formas_pagamento': FORMA_PAGAMENTO,
    }))


@admin_required
def excluir_movimento(request, pk):
    movimento = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        movimento.delete()
        messages.success(request, 'Movimento excluído com sucesso!')
        return redirect('financial_caixa_lista')
    return render(request, 'financial/confirmar_exclusao.html', {
        'object': movimento, 'is_admin': True
    })


@login_required
def extrato_caixa(request):
    movimentos = CashFlow.objects.all()
    saldo_acumulado = 0
    linhas = []
    for m in movimentos:
        if m.tipo == 'entrada':
            saldo_acumulado += m.valor
        else:
            saldo_acumulado -= m.valor
        linhas.append({
            'movimento': m,
            'saldo': saldo_acumulado,
        })

    total_entradas = sum(m.valor for m in movimentos if m.tipo == 'entrada')
    total_saidas = sum(m.valor for m in movimentos if m.tipo == 'saida')
    saldo_final = total_entradas - total_saidas

    return render(request, 'financial/caixa_extrato.html', add_user_context(request, {
        'linhas': linhas,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_final': saldo_final,
    }))


@login_required
def relatorio_caixa(request):
    movimentos = CashFlow.objects.all()
    meses = {}
    for m in movimentos:
        chave = m.data.strftime('%Y-%m')
        if chave not in meses:
            meses[chave] = {'entradas': 0, 'saidas': 0, 'mes': m.data.strftime('%B %Y')}
        if m.tipo == 'entrada':
            meses[chave]['entradas'] += float(m.valor)
        else:
            meses[chave]['saidas'] += float(m.valor)

    meses_ordenados = sorted(meses.items(), reverse=True)

    meses_com_saldo = []
    for chave, dados in meses_ordenados:
        meses_com_saldo.append({
            'chave': chave,
            'mes': dados['mes'],
            'entradas': dados['entradas'],
            'saidas': dados['saidas'],
            'saldo': dados['entradas'] - dados['saidas'],
        })

    return render(request, 'financial/caixa_relatorio.html', add_user_context(request, {
        'meses': meses_com_saldo,
    }))


# ─── Company Settings ─────────────────────────────────────────────

@admin_required
def config_assinatura(request):
    config, _ = CompanySettings.objects.get_or_create(pk=1)
    if request.method == 'POST':
        form = CompanySettingsForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações atualizadas com sucesso!')
            return redirect('financial_config_assinatura')
        messages.error(request, 'Corrija os erros do formulário.')
    else:
        form = CompanySettingsForm(instance=config)

    return render(request, 'financial/config_assinatura.html', add_user_context(request, {
        'config': config, 'form': form, 'is_admin': True
    }))
