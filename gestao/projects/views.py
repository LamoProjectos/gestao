from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
from crm.models import Client
from .models import Project, ProjectStage, TemplateEtapa
from financial.decorators import add_user_context, group_required


@login_required
def lista_projetos(request):
    projetos = Project.objects.all()
    return render(request, 'projects/lista.html', add_user_context(request, {'projetos': projetos}))


@group_required('Admin', 'Gestor')
def novo_projeto(request):
    clientes = Client.objects.all()
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        descricao = request.POST.get('descricao', '')
        valor_total = request.POST.get('valor_total', 0)
        data_inicio = request.POST.get('data_inicio', '') or None
        data_entrega = request.POST.get('data_entrega', '') or None
        importar_etapas = request.POST.get('importar_etapas') == 'on'

        if not nome or not cliente_id:
            messages.error(request, 'Preencha os campos obrigatórios.')
        else:
            projeto = Project.objects.create(
                cliente_id=cliente_id, nome=nome, tipo=tipo,
                descricao=descricao, valor_total=valor_total,
                data_inicio=data_inicio, data_entrega=data_entrega
            )
            if importar_etapas and tipo:
                templates = TemplateEtapa.objects.filter(tipo_projeto=tipo).order_by('ordem')
                data_ref = data_inicio or date.today()
                for t in templates:
                    data_prev = data_ref + timedelta(days=t.dias_apos_inicio) if data_ref else None
                    ProjectStage.objects.create(
                        projeto=projeto, ordem=t.ordem, nome=t.nome,
                        descricao=t.descricao, data_prevista=data_prev,
                    )
                messages.success(request, f'Projeto criado com {templates.count()} etapas importadas!')
            else:
                messages.success(request, 'Projeto criado com sucesso!')
            return redirect('projects_detalhe', pk=projeto.pk)

    return render(request, 'projects/form.html', add_user_context(request, {
        'clientes': clientes, 'titulo': 'Novo Projeto'
    }))


@login_required
def detalhe_projeto(request, pk):
    projeto = get_object_or_404(Project, pk=pk)
    etapas = projeto.etapas.all()
    return render(request, 'projects/detalhe.html', add_user_context(request, {
        'projeto': projeto, 'etapas': etapas,
    }))


@group_required('Admin', 'Gestor')
def editar_projeto(request, pk):
    projeto = get_object_or_404(Project, pk=pk)
    clientes = Client.objects.all()
    if request.method == 'POST':
        projeto.cliente_id = request.POST.get('cliente')
        projeto.nome = request.POST.get('nome')
        projeto.tipo = request.POST.get('tipo')
        projeto.status = request.POST.get('status')
        projeto.descricao = request.POST.get('descricao', '')
        projeto.valor_total = request.POST.get('valor_total', 0)
        projeto.data_inicio = request.POST.get('data_inicio', '') or None
        projeto.data_entrega = request.POST.get('data_entrega', '') or None
        projeto.save()
        messages.success(request, 'Projeto atualizado com sucesso!')
        return redirect('projects_detalhe', pk=projeto.pk)

    return render(request, 'projects/form.html', add_user_context(request, {
        'projeto': projeto, 'clientes': clientes, 'titulo': 'Editar Projeto'
    }))


@group_required('Admin')
def excluir_projeto(request, pk):
    projeto = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        projeto.delete()
        messages.success(request, 'Projeto excluído com sucesso!')
        return redirect('projects_lista')
    return render(request, 'projects/confirmar_exclusao.html', add_user_context(request, {
        'projeto': projeto
    }))


@group_required('Admin', 'Gestor')
def nova_etapa(request, pk):
    projeto = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        ordem = request.POST.get('ordem')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        data_prevista = request.POST.get('data_prevista', '') or None

        if not nome or not ordem:
            messages.error(request, 'Preencha os campos obrigatórios.')
        else:
            ProjectStage.objects.create(
                projeto=projeto, ordem=ordem, nome=nome,
                descricao=descricao, data_prevista=data_prevista
            )
            messages.success(request, 'Etapa adicionada com sucesso!')

    return redirect('projects_detalhe', pk=projeto.pk)


@group_required('Admin')
def excluir_etapa(request, pk):
    etapa = get_object_or_404(ProjectStage, pk=pk)
    projeto_pk = etapa.projeto.pk
    if request.method == 'POST':
        etapa.delete()
        messages.success(request, 'Etapa excluída com sucesso!')
    return redirect('projects_detalhe', pk=projeto_pk)


@group_required('Admin', 'Gestor', 'Engenheiro')
def concluir_etapa(request, pk):
    etapa = get_object_or_404(ProjectStage, pk=pk)
    if request.method == 'POST':
        if etapa.concluida:
            etapa.concluida = False
            etapa.data_conclusao = None
            messages.success(request, f'Etapa "{etapa.nome}" marcada como pendente.')
        else:
            etapa.concluida = True
            etapa.data_conclusao = date.today()
            messages.success(request, f'Etapa "{etapa.nome}" concluída!')
        etapa.save()
    return redirect('projects_detalhe', pk=etapa.projeto.pk)


@group_required('Admin', 'Gestor')
def importar_etapas_padrao(request, pk):
    projeto = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        templates = TemplateEtapa.objects.filter(tipo_projeto=projeto.tipo).order_by('ordem')
        if not templates:
            messages.warning(request, 'Não há etapas padrão definidas para este tipo de projeto.')
            return redirect('projects_detalhe', pk=pk)
        if projeto.etapas.exists():
            projeto.etapas.all().delete()
        data_ref = projeto.data_inicio or date.today()
        for t in templates:
            data_prev = data_ref + timedelta(days=t.dias_apos_inicio) if data_ref else None
            ProjectStage.objects.create(
                projeto=projeto, ordem=t.ordem, nome=t.nome,
                descricao=t.descricao, data_prevista=data_prev,
            )
        messages.success(request, f'{templates.count()} etapas importadas com sucesso!')
    return redirect('projects_detalhe', pk=pk)
