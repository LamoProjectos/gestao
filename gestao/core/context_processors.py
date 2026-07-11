from .models import Notification

def notificacoes_context(request):
    if request.user.is_authenticated:
        from django.db.models import Q
        nao_lidas = Notification.objects.filter(
            Q(user=request.user) | Q(user__isnull=True),
            lida=False,
        ).count()
        ultimas_notificacoes = Notification.objects.filter(
            Q(user=request.user) | Q(user__isnull=True),
        ).order_by('-criado_em')[:5]
        return {
            'notificacoes_nao_lidas': nao_lidas,
            'ultimas_notificacoes': ultimas_notificacoes,
        }
    return {}
