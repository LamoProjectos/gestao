from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    decorated = user_passes_test(
        lambda u: u.is_superuser,
        login_url='login'
    )(view_func)

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_superuser:
            messages.error(request, 'Apenas o administrador pode aceder a esta funcionalidade.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)

    wrapper.__name__ = view_func.__name__
    wrapper.__module__ = view_func.__module__
    return wrapper
