from django.shortcuts import render
from .models import Blog
from ProductsApp.models import PopularBrand
from django.shortcuts import render, get_object_or_404
# Create your views here.


def BlogView(request, *args, **kwargs):
    blogs = Blog.objects.filter(is_published=True).order_by('pub_date')
    
    context = {
        'blogs':blogs,
        'recent':Blog.objects.filter(is_published=True).order_by("-added_date")[:3],
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'blog/blog.html', context)

def BlogDetailView(request, slug, pk,*args, **kwargs):
    post = get_object_or_404(Blog, slug=slug, pk=pk)
    context = {
        'post':post,
    }
    return render(request, 'blog/blog-details.html', context)