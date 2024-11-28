from django.urls import path
from . import views
from .views import registro_login, sair

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('', views.IndexView.as_view(), name='index'),
    path('produtos/', views.ProdutosView.as_view(), name='produtos'),
    path('registro-login/', registro_login, name='registro_login'),
    path('sair/', sair, name='sair'),
]