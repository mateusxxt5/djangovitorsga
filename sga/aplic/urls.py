from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('', views.IndexView.as_view(), name='index'),
    path('produtos/', views.ProdutosView.as_view(), name='produtos'),
]