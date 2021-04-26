from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ["slug","image_thumbnail","created_at", "is_approved","added_by_merchant"]