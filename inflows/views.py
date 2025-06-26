from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from . import models, forms


ITEM_NAME = 'Entrada'
ITEM_NAME_PLURAL = 'Entradas'
RETURN_URL = 'inflow_list'


class InflowListView(LoginRequiredMixin, ListView):
    model = models.Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 10  # Define quantos itens por página
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name_plural'] = ITEM_NAME_PLURAL
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.GET.get('product')
        
        if product:
            queryset = queryset.filter(product__title__icontains=product)
            
        return queryset


class InflowCreateView(LoginRequiredMixin, CreateView):
    model = models.Inflow
    template_name = 'inflow_create.html'
    form_class = forms.InflowForm
    success_url = reverse_lazy(RETURN_URL)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context


class InflowDetailView(LoginRequiredMixin, DetailView):
    model = models.Inflow
    template_name = 'inflow_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.InflowDetailForm(instance=self.object)

        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        context['form'] = form
        return context