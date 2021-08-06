from django import forms
from .models import Products
from taggit.forms import TagWidget

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        images = forms.ImageField(label='Image', required=False)
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
                'class':'form-control col-lg-9'
            }),
            'product_long_description': forms.TextInput(attrs={
                'class':'form-control col-lg-9'
            }),
            'tags': TagWidget(attrs={
                'class':'form-control col-lg-9'
            }),
            'in_stock_total': forms.NumberInput(attrs={
                'class':'form-control col-lg-9'
            }),
            'images': forms.FileInput(attrs={
                'class':''})
        }