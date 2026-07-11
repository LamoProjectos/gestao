from datetime import date, timedelta
from django.contrib.auth.models import User
from .models import Notification

def criar_notificacao(user, tipo, mensagem, url=''):
    Notification.objects.create(
        user=user,
        tipo=tipo,
        mensagem=mensagem,
        url=url,
    )

def verificar_pagamentos_proximos():
    from financial.models import Payment
    hoje = date.today()
    limite = hoje + timedelta(days=5)
    pagamentos = Payment.objects.filter(
        status='pendente',
        data_vencimento__gte=hoje,
        data_vencimento__lte=limite,
    )
    for pag in pagamentos:
        msg = f'Pagamento {pag.prestacao}ª prestação de {pag.cotacao.numero} vence em {pag.data_vencimento}'
        url = f'/financial/cotacoes/{pag.cotacao.id}/'
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            if not Notification.objects.filter(mensagem=msg, user=admin, lida=False).exists():
                criar_notificacao(admin, 'warning', msg, url)

def verificar_etapas_proximas():
    from projects.models import ProjectStage
    hoje = date.today()
    limite = hoje + timedelta(days=5)
    etapas = ProjectStage.objects.filter(
        concluida=False,
        data_prevista__gte=hoje,
        data_prevista__lte=limite,
    )
    for etapa in etapas:
        msg = f'Etapa "{etapa.nome}" do projeto "{etapa.projeto.nome}" prevista para {etapa.data_prevista}'
        url = f'/projects/{etapa.projeto.id}/'
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            if not Notification.objects.filter(mensagem=msg, user=admin, lida=False).exists():
                criar_notificacao(admin, 'warning', msg, url)

def verificar_etapas_atrasadas():
    from projects.models import ProjectStage
    hoje = date.today()
    etapas = ProjectStage.objects.filter(
        concluida=False,
        data_prevista__lt=hoje,
    )
    for etapa in etapas:
        msg = f'⚠ Etapa "{etapa.nome}" do projeto "{etapa.projeto.nome}" está ATRASADA (prevista: {etapa.data_prevista})'
        url = f'/projects/{etapa.projeto.id}/'
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            if not Notification.objects.filter(mensagem=msg, user=admin, lida=False).exists():
                criar_notificacao(admin, 'danger', msg, url)

def verificar_pagamentos_atrasados():
    from financial.models import Payment
    hoje = date.today()
    pagamentos = Payment.objects.filter(
        status='pendente',
        data_vencimento__lt=hoje,
    )
    for pag in pagamentos:
        msg = f'⚠ Pagamento {pag.prestacao}ª prestação de {pag.cotacao.numero} está VENCIDO (vencia: {pag.data_vencimento})'
        url = f'/financial/cotacoes/{pag.cotacao.id}/'
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            if not Notification.objects.filter(mensagem=msg, user=admin, lida=False).exists():
                criar_notificacao(admin, 'danger', msg, url)
