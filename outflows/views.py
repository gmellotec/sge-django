from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from . import models, forms
from app import metrics


ITEM_NAME = 'Saída'
ITEM_NAME_PLURAL = 'Saídas'
RETURN_URL = 'outflow_list'


class OutflowListView(ListView):
    model = models.Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 10  # Define quantos itens por página
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name_plural'] = ITEM_NAME_PLURAL
        
        # Adicionar dados de metricas de produtos
        context['sales_metrics'] = metrics.get_sales_metrics
        
        return context
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.GET.get('product')
        
        if product:
            queryset = queryset.filter(product__title__icontains=product)
            
        return queryset


class OutflowCreateView(CreateView):
    model = models.Outflow
    template_name = 'outflow_create.html'
    form_class = forms.OutflowForm
    success_url = reverse_lazy(RETURN_URL)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context


class OutflowDetailView(DetailView):
    model = models.Outflow
    template_name = 'outflow_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.OutflowDetailForm(instance=self.object)

        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        context['form'] = form
        return context