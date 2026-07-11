from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Notification, AgendaEvent
from projects.models import Project, ProjectStage
from financial.models import Payment

@login_required
def agenda(request):
    eventos = []

    etapas = ProjectStage.objects.filter(projeto__isnull=False).select_related('projeto__cliente')
    for etapa in etapas:
        cor = 'success' if etapa.concluida else ('danger' if etapa.data_prevista and etapa.data_prevista < date.today() else 'warning')
        eventos.append({
            'titulo': etapa.nome,
            'descricao': f'{etapa.projeto.nome} — {etapa.descricao or "Sem descrição"}',
            'tipo': 'etapa',
            'data': etapa.data_prevista or date.today(),
            'cor': cor,
            'url': f'/projects/{etapa.projeto.id}/',
            'concluido': etapa.concluida,
        })

    pagamentos = Payment.objects.filter(status='pendente').select_related('cotacao__cliente')
    for pag in pagamentos:
        cor = 'danger' if pag.data_vencimento and pag.data_vencimento < date.today() else 'warning'
        eventos.append({
            'titulo': f'{pag.prestacao}ª Prestação — {pag.cotacao.numero}',
            'descricao': f'{pag.cotacao.cliente.nome} — {pag.valor} MZN',
            'tipo': 'pagamento',
            'data': pag.data_vencimento or date.today(),
            'cor': cor,
            'url': f'/financial/cotacoes/{pag.cotacao.id}/',
            'concluido': False,
        })

    projetos = Project.objects.all()
    for proj in projetos:
        if proj.data_inicio:
            eventos.append({
                'titulo': f'Início: {proj.nome}',
                'descricao': f'Cliente: {proj.cliente.nome}',
                'tipo': 'marco',
                'data': proj.data_inicio,
                'cor': 'success' if proj.status == 'concluido' else 'primary',
                'url': f'/projects/{proj.id}/',
                'concluido': proj.status == 'concluido',
            })
        if proj.data_entrega:
            cor = 'success' if proj.status == 'concluido' else ('danger' if proj.data_entrega < date.today() else 'primary')
            eventos.append({
                'titulo': f'Entrega: {proj.nome}',
                'descricao': f'Cliente: {proj.cliente.nome}',
                'tipo': 'marco',
                'data': proj.data_entrega,
                'cor': cor,
                'url': f'/projects/{proj.id}/',
                'concluido': proj.status == 'concluido',
            })

    eventos_por_data = {}
    for ev in eventos:
        d = ev['data']
        if d not in eventos_por_data:
            eventos_por_data[d] = []
        eventos_por_data[d].append(ev)

    datas_ordenadas = sorted(eventos_por_data.keys())

    filtro_tipo = request.GET.get('tipo', '')
    filtro_mes = request.GET.get('mes', '')

    return render(request, 'core/agenda.html', {
        'eventos_por_data': eventos_por_data,
        'datas_ordenadas': datas_ordenadas,
        'filtro_tipo': filtro_tipo,
        'filtro_mes': filtro_mes,
    })

@login_required
def notificacoes(request):
    notifs = Notification.objects.filter(
        Q(user=request.user) | Q(user__isnull=True)
    ).order_by('-criado_em')

    return render(request, 'core/notificacoes.html', {
        'notificacoes': notifs,
    })

@login_required
def marcar_lidas(request):
    Notification.objects.filter(
        Q(user=request.user) | Q(user__isnull=True),
        lida=False,
    ).update(lida=True)
    return redirect('core:notificacoes')
