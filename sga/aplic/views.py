from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import Produto

# Página principal
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['Produtos'] = Produto.objects.order_by('-nome').all()
        return context

# Página de Produtos
class ProdutosView(TemplateView):
    template_name = 'produtos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Produtos'] = Produto.objects.all()
        return context

# Login
class CustomLoginView(LoginView):
    template_name = 'login_cadastro.html'  # Template para a página de login
    redirect_authenticated_user = True  # Redireciona usuários logados para a home

# Cadastro
class CadastroView(FormView):
    template_name = 'login_cadastro.html'  # Mesmo template para login e cadastro
    form_class = UserCreationForm
    success_url = '/'  # Redirecionar após o cadastro

    def form_valid(self, form):
        user = form.save()  # Salva o novo usuário
        login(self.request, user)  # Loga o novo usuário automaticamente
        return redirect(self.success_url)  # Redireciona para a página principal
