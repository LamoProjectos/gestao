from datetime import date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crm.models import Client
from projects.models import Project, ProjectStage
from financial.models import Quote, Payment, CashFlow
from core.models import Tarefa

DIAS_URGENCIA = 7


@login_required
def home(request):
    total_clientes = Client.objects.count()
    projetos_ativos = Project.objects.filter(status__in=['proposta', 'aprovado', 'em_andamento']).count()
    projetos_concluidos = Project.objects.filter(status='concluido').count()

    hoje = date.today()
    limite = hoje + timedelta(days=5)

    # ── Faturamento ──
    inicio_mes = hoje.replace(day=1)

    def _mes_atras(inicio, n):
        y, m = inicio.year, inicio.month - n
        while m <= 0:
            m += 12
            y -= 1
        return date(y, m, 1)

    inicio_ano = date(hoje.year, 1, 1)

    faturado_mes = sum(
        q.valor_total for q in Quote.objects.filter(
            status='aprovada', data_emissao__gte=inicio_mes, data_emissao__lte=hoje))
    faturado_ano = sum(
        q.valor_total for q in Quote.objects.filter(
            status='aprovada', data_emissao__gte=inicio_ano, data_emissao__lte=hoje))
    recebido_mes = sum(
        m.valor for m in CashFlow.objects.filter(
            tipo='entrada', data__gte=inicio_mes, data__lte=hoje))

    # ── Gráfico: faturado vs recebido, últimos 6 meses ──
    meses_chart = []
    for i in range(5, -1, -1):
        mes_inicio = _mes_atras(inicio_mes, i)
        mes_fim = mes_inicio.replace(day=28) + timedelta(days=4)
        mes_fim = mes_fim.replace(day=1) - timedelta(days=1)
        faturado = sum(q.valor_total for q in Quote.objects.filter(
            status='aprovada', data_emissao__gte=mes_inicio, data_emissao__lte=mes_fim))
        recebido = sum(m.valor for m in CashFlow.objects.filter(
            tipo='entrada', data__gte=mes_inicio, data__lte=mes_fim))
        meses_chart.append({
            'rotulo': mes_inicio.strftime('%b'),
            'faturado': faturado,
            'recebido': recebido,
            'atual': mes_inicio.year == hoje.year and mes_inicio.month == hoje.month,
        })
    max_mes = max(
        [max(m['faturado'], m['recebido']) for m in meses_chart] or [0])

    # ── Propostas em jogo (cotações pendentes com dias restantes) ──
    cotacoes_pendentes_qs = Quote.objects.filter(status='pendente').select_related('cliente', 'projeto')
    propostas_urgentes = []
    propostas_normais = []
    for q in cotacoes_pendentes_qs:
        dias = q.dias_restantes()
        dados = {
            'cotacao': q,
            'dias': dias,
            'expirada': q.expirada,
        }
        if dias is not None and dias <= DIAS_URGENCIA:
            propostas_urgentes.append(dados)
        else:
            propostas_normais.append(dados)
    propostas_urgentes.sort(key=lambda x: x['dias'] if x['dias'] is not None else 999)

    cotacoes_pendentes = len(propostas_urgentes) + len(propostas_normais)

    # ── Projetos em execução (aprovado / em andamento) ──
    projetos_em_execucao = Project.objects.filter(
        status__in=['aprovado', 'em_andamento']
    ).select_related('cliente').order_by('data_entrega')

    # ── Detalhes financeiros por projeto (caixa preta) ──
    def _caixa_preta(projeto):
        movimentos = projeto.movimentos.all()
        entradas = sum(m.valor for m in movimentos if m.tipo == 'entrada')
        saidas = sum(m.valor for m in movimentos if m.tipo == 'saida')
        orcado = projeto.valor_total
        custo_real = saidas
        saldo = entradas - saidas
        margem = orcado - custo_real if orcado else None
        return {
            'orcado': orcado,
            'entradas': entradas,
            'saidas': saidas,
            'custo_real': custo_real,
            'saldo': saldo,
            'margem': margem,
            'n_movimentos': movimentos.count(),
        }

    execucao_detalhe = []
    for p in projetos_em_execucao:
        cp = _caixa_preta(p)
        cp['projeto'] = p
        execucao_detalhe.append(cp)

    # ── Caixa ──
    movimentos = CashFlow.objects.all()
    total_entradas = sum(m.valor for m in movimentos if m.tipo == 'entrada')
    total_saidas = sum(m.valor for m in movimentos if m.tipo == 'saida')
    saldo_caixa = total_entradas - total_saidas
    ultimos_movimentos = CashFlow.objects.order_by('-data', '-criado_em')[:5]

    # ── Listas recentes ──
    ultimos_clientes = Client.objects.order_by('-criado_em')[:5]
    ultimos_projetos = Project.objects.order_by('-criado_em')[:5]
    ultimas_cotacoes = Quote.objects.order_by('-criado_em')[:5]

    # ── Tarefas de hoje e atrasadas ──
    tarefas_hoje = Tarefa.objects.filter(data=hoje).select_related('projeto')
    tarefas_atrasadas = Tarefa.objects.filter(concluida=False, data__lt=hoje).select_related('projeto')

    # ── Alertas ──
    pagamentos_pendentes = Payment.objects.filter(status='pendente')
    total_pendente = sum(p.valor for p in pagamentos_pendentes)

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
        'hoje': hoje,
        'total_clientes': total_clientes,
        'projetos_ativos': projetos_ativos,
        'projetos_concluidos': projetos_concluidos,
        'cotacoes_pendentes': cotacoes_pendentes,
        'total_pendente': total_pendente,
        'faturado_mes': faturado_mes,
        'faturado_ano': faturado_ano,
        'recebido_mes': recebido_mes,
        'meses_chart': meses_chart,
        'max_mes': max_mes,
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
        'propostas_urgentes': propostas_urgentes,
        'propostas_normais': propostas_normais,
        'execucao_detalhe': execucao_detalhe,
        'tarefas_hoje': tarefas_hoje,
        'tarefas_atrasadas': tarefas_atrasadas,
    })
