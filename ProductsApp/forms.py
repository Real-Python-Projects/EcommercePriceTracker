from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ["slug","image_thumbnail","created_at", "is_approved","added_by_merchant","view_count"]
        
        widgets = {
            'category': forms.Select(attrs={
                'class':'form-control col-lg-9'
            }),
            'product_name': forms.TextInput(attrs={
                'class':'form-control col-lg-9'
            }),
            'brand': forms.TextInput(attrs={
                'class':'form-control col-lg-9'
            }),
            'product_max_price': forms.TextInput(attrs={
                'class':'form-control col-lg-9'
            }),
            'product_discount_price': forms.TextInput(attrs={
                'class':'form-control col-lg-9'
            }),
            'product_description': forms.TextInput(attrs={
                'class':'form-control'
            }),
            'product_long_description': forms.TextInput(attrs={
                'class':'form-control'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class':'form-control'
            }),
            'in_stock_total': forms.NumberInput(attrs={
                'class':'form-control col-lg-9'
            })
        }