from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms


ITEM_NAME = 'Fornecedor'
ITEM_NAME_PLURAL = 'Fornecedores'
RETURN_URL = 'supplier_list'


class SupplierListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Supplier
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10  # Define quantos itens por página
    permission_required = 'suppliers.view_supplier'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
            
        return queryset.order_by('id')


class SupplierCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Supplier
    template_name = 'supplier_create.html'
    form_class = forms.SupplierForm
    success_url = reverse_lazy(RETURN_URL)
    permission_required = 'suppliers.add_supplier'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context


class SupplierDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Supplier
    template_name = 'supplier_detail.html'  # novo template
    permission_required = 'suppliers.view_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.SupplierForm(instance=self.object)

        # Desabilitar todos os campos
        for field in form.fields.values():
            field.widget.attrs['disabled'] = True

        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        context['form'] = form
        return context    
    
    
class SupplierUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Supplier
    template_name = 'supplier_update.html'
    form_class = forms.SupplierForm
    success_url = reverse_lazy(RETURN_URL)
    permission_required = 'suppliers.change_supplier'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context
    

class SupplierDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Supplier
    template_name = 'supplier_delete.html'
    success_url = reverse_lazy(RETURN_URL)
    permission_required = 'suppliers.delete_supplier'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context