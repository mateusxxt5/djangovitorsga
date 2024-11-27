from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .models import Produto, Categoria

# Página principal
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['Produtos'] = Produto.objects.order_by('-nome').all()
        return context

# Página de Produtos
class ProdutosView(ListView):
    model = Produto
    template_name = 'produtos.html'
    context_object_name = 'Produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Categorias'] = Categoria.objects.all()
        
        # Filtro de categoria
        categoria_selecionada = self.request.GET.get('categoria')
        context['Categoria_Selecionada'] = categoria_selecionada
        
        return context

    def get_queryset(self):
        queryset = Produto.objects.all()
        categoria_selecionada = self.request.GET.get('categoria')
        
        if categoria_selecionada:
            queryset = queryset.filter(categoria__id=categoria_selecionada)
        
        return queryset

# Outras views permanecem as mesmas
class CustomLoginView(LoginView):
    template_name = 'login_cadastro.html'
    redirect_authenticated_user = True

class CadastroView(FormView):
    template_name = 'login_cadastro.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)