from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
from crm.models import Client
from .models import Project, ProjectStage, TemplateEtapa
from .forms import ProjectForm, ProjectStageForm
from financial.decorators import add_user_context, group_required


@login_required
def lista_projetos(request):
    projetos = Project.objects.all()
    return render(request, 'projects/lista.html', add_user_context(request, {'projetos': projetos}))


@group_required('Admin', 'Gestor')
def novo_projeto(request):
    clientes = Client.objects.all()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            projeto = form.save()
            tipo = form.cleaned_data['tipo']
            if form.cleaned_data['importar_etapas'] and tipo:
                templates = TemplateEtapa.objects.filter(tipo_projeto=tipo).order_by('ordem')
                data_ref = projeto.data_inicio or date.today()
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
        messages.error(request, 'Corrija os erros do formulário.')

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
        form = ProjectForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto atualizado com sucesso!')
            return redirect('projects_detalhe', pk=projeto.pk)
        messages.error(request, 'Corrija os erros do formulário.')
    else:
        form = ProjectForm(instance=projeto)

    return render(request, 'projects/form.html', add_user_context(request, {
        'projeto': projeto, 'clientes': clientes, 'form': form, 'titulo': 'Editar Projeto'
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
        form = ProjectStageForm(request.POST)
        if form.is_valid():
            etapa = form.save(commit=False)
            etapa.projeto = projeto
            etapa.save()
            messages.success(request, 'Etapa adicionada com sucesso!')
        else:
            messages.error(request, 'Corrija os erros do formulário.')

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
