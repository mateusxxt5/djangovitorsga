from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .models import Produto, Categoria
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ClienteForm
from .models import Cliente

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
    

def registro_login(request):
    if request.method == 'POST':
        # Verificar se é um formulário de login
        if 'email_login' in request.POST:
            email = request.POST['email_login']
            senha = request.POST['senha_login']
            user = authenticate(request, username=email, password=senha)
            if user is not None:
                login(request, user)
                return redirect('pagina_inicial')
            else:
                messages.error(request, 'Credenciais inválidas')

        # Verificar se é um formulário de cadastro
        elif 'email' in request.POST:
            form = ClienteForm(request.POST)
            if form.is_valid():
                # Cria usuário no sistema de autenticação do Django
                user = user.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['senha']
                )
                
                # Cria cliente no modelo personalizado
                cliente = form.save(commit=False)
                cliente.user = user  # Adicione um campo user no modelo Cliente
                cliente.save()
                
                login(request, user)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('pagina_inicial')
            else:
                # Renderiza o formulário novamente com os erros
                return render(request, 'registro_login.html', {'form': form})

    # Se for GET, renderiza o formulário em branco
    form = ClienteForm()
    return render(request, 'registro_login.html', {'form': form})

def sair(request):
    logout(request)
    return redirect('pagina_inicial')