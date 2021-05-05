from django import forms

from .models import Blog

class BlogCreateForm(forms.ModelForm):
    class Meta:
        models=Blog