from django import forms
from .models import Products
from tinymce.widgets import TinyMCE

class ProductForm(forms.ModelForm):
    product_description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows':10}))
    product_long_description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows':10}))
    class Meta:
        model = Products
        exclude = ["slug","image_thumbnail","created_at", "is_approved","added_by_merchant"]