import io
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from pathlib import Path
from weasyprint import HTML
from financial.models import Quote, Payment, CompanySettings


def _get_config():
    config = CompanySettings.objects.filter(pk=1).first()
    assinatura_path = None
    if config and config.assinatura:
        p = Path(config.assinatura.path)
        if p.exists():
            assinatura_path = str(p.resolve())
    if not assinatura_path:
        for base in [settings.BASE_DIR / 'static', settings.STATIC_ROOT]:
            p = base / 'img' / 'assinatura.png'
            if p.exists():
                assinatura_path = str(p.resolve())
                break
    return {
        'config': config,
        'assinatura_path': assinatura_path,
        'data_hoje': timezone.now().date(),
    }


@login_required
def gerar_cotacao_pdf(request, pk):
    if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
        return HttpResponse('Acesso negado. Apenas o administrador.', status=403)
    cotacao = get_object_or_404(Quote, pk=pk)
    pagamentos = cotacao.pagamentos.all()
    ctx = _get_config()
    ctx.update({'cotacao': cotacao, 'pagamentos': pagamentos})

    html = render_to_string('documents/cotacao_pdf.html', ctx)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="cotacao_{cotacao.numero}.pdf"'
    HTML(string=html).write_pdf(response)
    return response


@login_required
def gerar_recibo_pdf(request, pk):
    if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
        return HttpResponse('Acesso negado. Apenas o administrador.', status=403)
    pagamento = get_object_or_404(Payment, pk=pk)
    ctx = _get_config()
    ctx.update({'pagamento': pagamento})

    html = render_to_string('documents/recibo_pdf.html', ctx)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="recibo_{pagamento.cotacao.numero}_{pagamento.prestacao}.pdf"'
    HTML(string=html).write_pdf(response)
    return response


@login_required
def gerar_contrato_pdf(request, pk):
    if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
        return HttpResponse('Acesso negado. Apenas o administrador.', status=403)
    from projects.models import Project
    projeto = get_object_or_404(Project, pk=pk)
    ctx = _get_config()
    ctx.update({'projeto': projeto})

    html = render_to_string('documents/contrato_pdf.html', ctx)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="contrato_{projeto.cliente.nome}.pdf"'
    HTML(string=html).write_pdf(response)
    return response
