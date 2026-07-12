from .models import Notification


def notificacoes_context(request):
    ctx = {}
    if request.user.is_authenticated:
        from django.db.models import Q
        nao_lidas = Notification.objects.filter(
            Q(user=request.user) | Q(user__isnull=True),
            lida=False,
        ).count()
        ultimas_notificacoes = Notification.objects.filter(
            Q(user=request.user) | Q(user__isnull=True),
        ).order_by('-criado_em')[:5]
        ctx.update({
            'notificacoes_nao_lidas': nao_lidas,
            'ultimas_notificacoes': ultimas_notificacoes,
        })
        ctx['is_admin'] = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
        ctx['is_gestor'] = ctx['is_admin'] or request.user.groups.filter(name='Gestor').exists()
        ctx['is_engenheiro'] = ctx['is_gestor'] or request.user.groups.filter(name='Engenheiro').exists()
    return ctx
