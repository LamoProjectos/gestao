from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
