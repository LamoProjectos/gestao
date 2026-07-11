from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client

@login_required
def lista_clientes(request):
    busca = request.GET.get('busca', '')
    if busca:
        clientes = Client.objects.filter(nome__icontains=busca)
    else:
        clientes = Client.objects.all()
    return render(request, 'crm/lista.html', {'clientes': clientes, 'busca': busca})

@login_required
def novo_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone', '')
        email = request.POST.get('email', '')
        endereco = request.POST.get('endereco', '')
        nuit = request.POST.get('nuit', '')
        observacoes = request.POST.get('observacoes', '')

        if not nome:
            messages.error(request, 'O nome do cliente é obrigatório.')
        else:
            Client.objects.create(
                nome=nome, telefone=telefone, email=email,
                endereco=endereco, nuit=nuit, observacoes=observacoes
            )
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('crm_lista')

    return render(request, 'crm/form.html', {'titulo': 'Novo Cliente'})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        cliente.nome = request.POST.get('nome')
        cliente.telefone = request.POST.get('telefone', '')
        cliente.email = request.POST.get('email', '')
        cliente.endereco = request.POST.get('endereco', '')
        cliente.nuit = request.POST.get('nuit', '')
        cliente.observacoes = request.POST.get('observacoes', '')
        cliente.save()
        messages.success(request, 'Cliente atualizado com sucesso!')
        return redirect('crm_lista')

    return render(request, 'crm/form.html', {'cliente': cliente, 'titulo': 'Editar Cliente'})

@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('crm_lista')
    return render(request, 'crm/confirmar_exclusao.html', {'cliente': cliente})
