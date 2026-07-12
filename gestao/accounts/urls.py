from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
    path('utilizadores/', views.lista_utilizadores, name='lista_utilizadores'),
    path('utilizadores/novo/', views.novo_utilizador, name='novo_utilizador'),
    path('utilizadores/<int:pk>/editar/', views.editar_utilizador, name='editar_utilizador'),
    path('utilizadores/<int:pk>/desativar/', views.desativar_utilizador, name='desativar_utilizador'),
    path('utilizadores/<int:pk>/reativar/', views.reativar_utilizador, name='reativar_utilizador'),
]
