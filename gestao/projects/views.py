from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from crm.models import Client
from .models import Project, ProjectStage

@login_required
def lista_projetos(request):
    projetos = Project.objects.all()
    return render(request, 'projects/lista.html', {'projetos': projetos})

@login_required
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

        if not nome or not cliente_id:
            messages.error(request, 'Preencha os campos obrigatórios.')
        else:
            Project.objects.create(
                cliente_id=cliente_id, nome=nome, tipo=tipo,
                descricao=descricao, valor_total=valor_total,
                data_inicio=data_inicio, data_entrega=data_entrega
            )
            messages.success(request, 'Projeto criado com sucesso!')
            return redirect('projects_lista')

    return render(request, 'projects/form.html', {'clientes': clientes, 'titulo': 'Novo Projeto'})

@login_required
def detalhe_projeto(request, pk):
    projeto = get_object_or_404(Project, pk=pk)
    etapas = projeto.etapas.all()
    return render(request, 'projects/detalhe.html', {'projeto': projeto, 'etapas': etapas})

@login_required
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

    return render(request, 'projects/form.html', {
        'projeto': projeto, 'clientes': clientes, 'titulo': 'Editar Projeto'
    })

@login_required
def excluir_projeto(request, pk):
    projeto = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        projeto.delete()
        messages.success(request, 'Projeto excluído com sucesso!')
        return redirect('projects_lista')
    return render(request, 'projects/confirmar_exclusao.html', {'projeto': projeto})

@login_required
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

@login_required
def excluir_etapa(request, pk):
    etapa = get_object_or_404(ProjectStage, pk=pk)
    projeto_pk = etapa.projeto.pk
    if request.method == 'POST':
        etapa.delete()
        messages.success(request, 'Etapa excluída com sucesso!')
    return redirect('projects_detalhe', pk=projeto_pk)
