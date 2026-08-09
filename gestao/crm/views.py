from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client
from .forms import ClientForm

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
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('crm_lista')
        messages.error(request, 'Corrija os erros do formulário.')
    else:
        form = ClientForm()
    return render(request, 'crm/form.html', {'form': form, 'titulo': 'Novo Cliente'})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('crm_lista')
        messages.error(request, 'Corrija os erros do formulário.')
    else:
        form = ClientForm(instance=cliente)
    return render(request, 'crm/form.html', {'form': form, 'cliente': cliente, 'titulo': 'Editar Cliente'})

@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('crm_lista')
    return render(request, 'crm/confirmar_exclusao.html', {'cliente': cliente})
