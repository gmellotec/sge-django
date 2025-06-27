from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms


ITEM_NAME = 'Categoria'
ITEM_NAME_PLURAL = 'Categorias'
RETURN_URL = 'category_list'


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 10  # Define quantos itens por página
    permission_required = 'categories.view_category'
    
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


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Category
    template_name = 'category_create.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy(RETURN_URL)
    permission_required = 'categories.add_category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context


class CategoryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Category
    template_name = 'category_detail.html'  # novo template
    permission_required = 'categories.view_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.CategoryForm(instance=self.object)

        # Desabilitar todos os campos
        for field in form.fields.values():
            field.widget.attrs['disabled'] = True

        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        context['form'] = form
        return context    
    
    
class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Category
    template_name = 'category_update.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy(RETURN_URL)
    permission_required = 'categories.change_category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context
    

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy(RETURN_URL)
    permission_required = 'categories.delete_category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_name'] = ITEM_NAME
        context['item_name_plural'] = ITEM_NAME_PLURAL
        context['return_url'] = RETURN_URL
        return context