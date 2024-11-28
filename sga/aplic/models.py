import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone  # Importe esta biblioteca
from django.conf import settings  # Importe settings

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Use esta referência 
        on_delete=models.CASCADE,
        default=1  # Assume que existe um usuário com ID 1
    )
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        default='000.000.000-00',
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 
                message='CPF deve estar no formato XXX.XXX.XXX-XX'
            )
        ]
    )
    data_nascimento = models.DateField(default=timezone.now)
    endereco = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente.nome}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome}'
from django.db import models
