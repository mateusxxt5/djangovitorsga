from django.contrib import admin
from .models import Categoria, Produto, Cliente, Pedido, ItemPedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')  # Exibe os campos no painel
    search_fields = ('nome',)  # Campo de busca

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'categoria', 'data_criacao', 'descricao', 'imagem')  # Exibe os campos no painel
    list_filter = ('categoria', 'data_criacao')  # Filtros laterais
    search_fields = ('nome', 'descricao')  # Campo de busca
    list_editable = ('preco', 'descricao', 'imagem')  # Permite editar diretamente na lista

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')  # Exibe os campos no painel
    search_fields = ('nome', 'email')  # Campo de busca

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1  # Número de linhas extras para adicionar

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_pedido', 'total')  # Exibe os campos no painel
    list_filter = ('data_pedido',)  # Filtros laterais
    search_fields = ('cliente__nome',)  # Campo de busca por cliente
    inlines = [ItemPedidoInline]  # Permite adicionar itens do pedido no mesmo formulário

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'produto', 'quantidade')  # Exibe os campos no painel
    list_filter = ('pedido', 'produto')  # Filtros laterais
    search_fields = ('produto__nome',)  # Campo de busca por produto
    