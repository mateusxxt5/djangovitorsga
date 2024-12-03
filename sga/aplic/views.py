from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Produto, Categoria, Cliente, Pedido, ItemPedido
from .forms import ClienteCreationForm


# Página principal
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.order_by('-data_criacao')[:10]  # Ordena por data de criação
        return context


# Página de Produtos
class ProdutosView(ListView):
    model = Produto
    template_name = 'produtos.html'
    context_object_name = 'produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Todas as categorias
        categoria_selecionada = self.request.GET.get('categoria')
        context['categoria_selecionada'] = categoria_selecionada  # Define a categoria selecionada
        return context

    def get_queryset(self):
        queryset = Produto.objects.all()
        categoria_id = self.request.GET.get('categoria')  # Obtém o ID da categoria da query string
        if categoria_id:  # Se houver uma categoria selecionada
            queryset = queryset.filter(categoria__id=categoria_id)
        return queryset

def listar_produtos(request):
    categorias = Categoria.objects.all()
    categoria_selecionada = request.GET.get('categoria')  # Obter categoria selecionada
    if categoria_selecionada:
        produtos = Produto.objects.filter(categoria__id=categoria_selecionada)
    else:
        produtos = Produto.objects.all()

    return render(request, 'produtos.html', {
        'categorias': categorias,
        'produtos': produtos,
        'categoria_selecionada': categoria_selecionada
    })


@login_required
def carrinho(request):
    pedido = Pedido.objects.filter(cliente=request.user, status='A').first()
    itens = pedido.itens.all() if pedido else []
    return render(request, 'carrinho.html', {'pedido': pedido, 'itens': itens})


@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))  # Obtém a quantidade do formulário
    pedido, created = Pedido.objects.get_or_create(cliente=request.user, status='A')  # Pedido ativo

    # Verifica se o item já está no pedido
    item, item_created = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)
    if not item_created:
        item.quantidade += quantidade
    else:
        item.quantidade = quantidade

    item.preco_unitario = produto.preco
    item.subtotal = item.quantidade * item.preco_unitario
    item.save()

    # Atualiza o total do pedido
    pedido.calcular_total()

    messages.success(request, f"{produto.nome} adicionado ao carrinho.")
    return redirect('carrinho')


@login_required
def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemPedido, id=item_id, pedido__cliente=request.user, pedido__status='A')
    if item:
        pedido = item.pedido
        item.delete()
        pedido.calcular_total()
        messages.success(request, "Item removido do carrinho.")
    else:
        messages.error(request, "O item não existe ou já foi removido.")
    return redirect('carrinho')


@login_required
def finalizar_compra(request):
    pedido = get_object_or_404(Pedido, cliente=request.user, status='A')
    if pedido.itens.exists():
        pedido.status = 'F'
        pedido.save()
        messages.success(request, "Compra finalizada com sucesso!")
    else:
        messages.error(request, "Não é possível finalizar um pedido vazio.")
    return redirect('index')


# Login e Cadastro Unificado
def registro_login(request):
    form = ClienteCreationForm()  # Inicializa o formulário sempre

    if request.method == 'POST':
        # Verificar se é login
        if 'username_login' in request.POST:
            username = request.POST.get('username_login')
            senha = request.POST.get('senha_login')
            user = authenticate(request, username=username, password=senha)
            if user:
                login(request, user)
                messages.success(request, f"Bem-vindo(a), {user.username}! Login realizado com sucesso.")
                return redirect('index')  # Redirecionar para a página inicial
            else:
                messages.error(request, "Usuário ou senha inválidos. Tente novamente.")
                return redirect('login')

        # Verificar se é cadastro
        elif 'username' in request.POST:
            form = ClienteCreationForm(request.POST)  # Recria o formulário com os dados POST
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Cadastro realizado com sucesso! Você está logado.")
                return redirect('index')  # Redirecionar para a página inicial após cadastro
            else:
                messages.error(request, "Erro no cadastro. Verifique os dados fornecidos.")

    return render(request, 'login_cadastro.html', {'form': form})

# Logout
@login_required
def sair(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta com sucesso.")
    return redirect('index')
