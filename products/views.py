from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from . import models, forms
from brands.models import Brand
from categories.models import Category
from app import metrics


ITEM_NAME = 'Produto'
ITEM_NAME_PLURAL = 'Produtos'
RETURN_URL = 'product_list'


class ProductListView(LoginRequiredMixin, ListView):
    model = models.Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10  # Define quantos itens por página
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        serie_number = self.request.GET.get('serie_number')
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        
        if title:
            queryset = queryset.filter(title__icontains=title)
            
        if serie_number:
            queryset = queryset.filter(serie_number__icontains=serie_number)
            
        if category:
            queryset = queryset.filter(category__id=category)
            
        if brand:
            queryset = queryset.filter(brand__id=brand)
            
        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        
        # Adicionar dados de metricas de produtos
        context['product_metrics'] = metrics.get_product_metrics
        
        # Inserir os dados no contexto para poder ter acesso a eles no template
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        return context
    

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = models.Product
    template_name = 'product_create.html'
    form_class = forms.ProductForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        # Adicionar contexto de sucesso para mostrar o modal
        context = self.get_context_data()
        context['show_success_modal'] = True
        context['success_message'] = f'{ITEM_NAME} "{self.object.title}" cadastrado com sucesso!'
        context['redirect_url'] = reverse_lazy(RETURN_URL)
        return self.render_to_response(context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = models.Product
    template_name = 'product_detail.html'  # novo template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.ProductForm(instance=self.object)

        # Desabilitar todos os campos
        for field in form.fields.values():
            field.widget.attrs['disabled'] = True

        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        context['form'] = form
        return context    
    
    
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Product
    template_name = 'product_update.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy(RETURN_URL)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context
    

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy(RETURN_URL)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context