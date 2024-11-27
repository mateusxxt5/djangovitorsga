from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Produto

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['Produtos'] = Produto.objects.order_by('-nome').all()
        return context