from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from financial.decorators import admin_required, add_user_context


@login_required
def alterar_senha(request):
    if request.method == 'POST':
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not request.user.check_password(senha_atual):
            messages.error(request, 'Senha atual incorreta.')
        elif nova_senha != confirmar_senha:
            messages.error(request, 'As novas senhas não coincidem.')
        elif len(nova_senha) < 4:
            messages.error(request, 'A nova senha deve ter pelo menos 4 caracteres.')
        else:
            request.user.set_password(nova_senha)
            request.user.save()
            messages.success(request, 'Senha alterada com sucesso! Faça login novamente.')
            return redirect('login')

    return render(request, 'accounts/alterar_senha.html')


@admin_required
def lista_utilizadores(request):
    utilizadores = User.objects.all().order_by('username')
    grupos = Group.objects.all()
    return render(request, 'accounts/lista.html', add_user_context(request, {
        'utilizadores': utilizadores,
        'grupos': grupos,
    }))


@admin_required
def novo_utilizador(request):
    grupos = Group.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '')
        grupos_ids = request.POST.getlist('grupos')

        if not username or not password:
            messages.error(request, 'Utilizador e senha são obrigatórios.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de utilizador já existe.')
        elif len(password) < 4:
            messages.error(request, 'A senha deve ter pelo menos 4 caracteres.')
        else:
            user = User.objects.create_user(
                username=username, email=email,
                password=password, first_name=first_name,
                is_staff=True,
            )
            user.groups.set(grupos_ids)
            messages.success(request, f'Utilizador "{username}" criado com sucesso!')
            return redirect('accounts:lista_utilizadores')

    return render(request, 'accounts/form.html', add_user_context(request, {
        'grupos': grupos, 'titulo': 'Novo Utilizador'
    }))


@admin_required
def editar_utilizador(request, pk):
    user = get_object_or_404(User, pk=pk)
    grupos = Group.objects.all()
    if request.method == 'POST':
        user.email = request.POST.get('email', '')
        user.first_name = request.POST.get('first_name', '')
        user.is_active = request.POST.get('is_active') == 'on'
        password = request.POST.get('password', '')
        grupos_ids = request.POST.getlist('grupos')

        if password:
            if len(password) < 4:
                messages.error(request, 'A senha deve ter pelo menos 4 caracteres.')
                return render(request, 'accounts/form.html', add_user_context(request, {
                    'user': user, 'grupos': grupos, 'titulo': 'Editar Utilizador'
                }))
            user.set_password(password)

        user.save()
        user.groups.set(grupos_ids)
        messages.success(request, f'Utilizador "{user.username}" atualizado com sucesso!')
        return redirect('accounts:lista_utilizadores')

    return render(request, 'accounts/form.html', add_user_context(request, {
        'user': user, 'grupos': grupos, 'titulo': 'Editar Utilizador'
    }))


@admin_required
def desativar_utilizador(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, 'Não podes desativar a tua própria conta.')
        return redirect('accounts:lista_utilizadores')
    if request.method == 'POST':
        user.is_active = False
        user.save()
        messages.success(request, f'Utilizador "{user.username}" desativado com sucesso!')
        return redirect('accounts:lista_utilizadores')
    return render(request, 'accounts/confirmar_exclusao.html', {'user': user, 'is_admin': True})


@admin_required
def reativar_utilizador(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    messages.success(request, f'Utilizador "{user.username}" reativado com sucesso!')
    return redirect('accounts:lista_utilizadores')
