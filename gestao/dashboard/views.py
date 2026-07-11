from datetime import date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crm.models import Client
from projects.models import Project, ProjectStage
from financial.models import Quote, Payment, CashFlow

@login_required
def home(request):
    total_clientes = Client.objects.count()
    projetos_ativos = Project.objects.filter(status__in=['proposta', 'aprovado', 'em_andamento']).count()
    projetos_concluidos = Project.objects.filter(status='concluido').count()
    cotacoes_pendentes = Quote.objects.filter(status='pendente').count()

    pagamentos_pendentes = Payment.objects.filter(status='pendente')
    total_pendente = sum(p.valor for p in pagamentos_pendentes)

    movimentos = CashFlow.objects.all()
    total_entradas = sum(m.valor for m in movimentos if m.tipo == 'entrada')
    total_saidas = sum(m.valor for m in movimentos if m.tipo == 'saida')
    saldo_caixa = total_entradas - total_saidas
    ultimos_movimentos = CashFlow.objects.order_by('-data', '-criado_em')[:5]

    ultimos_clientes = Client.objects.order_by('-criado_em')[:5]
    ultimos_projetos = Project.objects.order_by('-criado_em')[:5]
    ultimas_cotacoes = Quote.objects.order_by('-criado_em')[:5]

    hoje = date.today()
    limite = hoje + timedelta(days=5)

    pagamentos_proximos = Payment.objects.filter(
        status='pendente',
        data_vencimento__gte=hoje,
        data_vencimento__lte=limite,
    ).select_related('cotacao__cliente').order_by('data_vencimento')

    pagamentos_atrasados = Payment.objects.filter(
        status='pendente',
        data_vencimento__lt=hoje,
    ).select_related('cotacao__cliente').order_by('data_vencimento')

    etapas_proximas = ProjectStage.objects.filter(
        concluida=False,
        data_prevista__gte=hoje,
        data_prevista__lte=limite,
    ).select_related('projeto__cliente').order_by('data_prevista')

    etapas_atrasadas = ProjectStage.objects.filter(
        concluida=False,
        data_prevista__lt=hoje,
    ).select_related('projeto__cliente').order_by('data_prevista')

    return render(request, 'dashboard/home.html', {
        'total_clientes': total_clientes,
        'projetos_ativos': projetos_ativos,
        'projetos_concluidos': projetos_concluidos,
        'cotacoes_pendentes': cotacoes_pendentes,
        'total_pendente': total_pendente,
        'saldo_caixa': saldo_caixa,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'ultimos_movimentos': ultimos_movimentos,
        'ultimos_clientes': ultimos_clientes,
        'ultimos_projetos': ultimos_projetos,
        'ultimas_cotacoes': ultimas_cotacoes,
        'pagamentos_proximos': pagamentos_proximos,
        'pagamentos_atrasados': pagamentos_atrasados,
        'etapas_proximas': etapas_proximas,
        'etapas_atrasadas': etapas_atrasadas,
    })
