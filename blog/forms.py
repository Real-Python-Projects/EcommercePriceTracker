from django import forms

from .models import Blog

class BlogCreateForm(forms.ModelForm):
    class Meta:
        models=Blog
        exclude = ["author", "added_date","pub_date"]
        
        
class BlogFormMedia(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ["post","timestamp"]