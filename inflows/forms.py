from django import forms
from . import models


class InflowForm(forms.ModelForm):
    
    class Meta:
        model = models.Inflow
        fields = ['product', 'supplier', 'quantity', 'description']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
        labels = {
            'product': 'Produto',
            'supplier': 'Fornecedor',
            'quantity': 'Quantidade',
            'description': 'Descrição',
        }
        
        
class InflowDetailForm(forms.ModelForm):
    created_at = forms.DateTimeField(
        label='Data de Entrada',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'disabled': True}),
        required=False
    )

    class Meta:
        model = models.Inflow
        fields = ['product', 'supplier', 'quantity', 'description']  # Não incluir created_at aqui

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'product': 'Produto',
            'supplier': 'Fornecedor',
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