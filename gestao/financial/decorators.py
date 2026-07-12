from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'Apenas o administrador pode aceder a esta funcionalidade.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return wrapper


def group_required(*group_names):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.is_superuser or request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            messages.error(request, 'Não tens permissão para aceder a esta funcionalidade.')
            return redirect('dashboard:home')
        return wrapper
    return decorator


def add_user_context(request, context=None):
    if context is None:
        context = {}
    context['is_admin'] = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
    context['is_gestor'] = context['is_admin'] or request.user.groups.filter(name='Gestor').exists()
    context['is_engenheiro'] = context['is_gestor'] or request.user.groups.filter(name='Engenheiro').exists()
    return context
