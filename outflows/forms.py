from django import forms
from django.core.exceptions import ValidationError
from . import models


class OutflowForm(forms.ModelForm):
    
    
    class Meta:
        model = models.Outflow
        fields = ['product', 'quantity', 'description']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
        labels = {
            'product': 'Produto',
            'quantity': 'Quantidade',
            'description': 'Descrição',
        }
        
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        
        if quantity > product.quantity:
            raise ValidationError(
                f'A quantidade disponível em estoque para o produto "{product.title}" é de {product.quantity} unidades.'
            )
        
        return quantity


class OutflowDetailForm(forms.ModelForm):
    created_at = forms.DateTimeField(
        label='Data de Saída',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'disabled': True}),
        required=False
    )


    class Meta:
        model = models.Outflow
        fields = ['product', 'quantity', 'description']  # Não incluir created_at aqui

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'product': 'Produto',
            'quantity': 'Quantidade',
            'description': 'Descrição',
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Atribuir valor ao campo manualmente com base na instância
        if self.instance and self.instance.pk:
            self.fields['created_at'].initial = self.instance.created_at

        # Desabilitar os campos do Meta manualmente
        for field_name in self.Meta.fields:
            self.fields[field_name].widget.attrs['disabled'] = True