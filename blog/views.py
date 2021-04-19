from django.shortcuts import render
from .models import Blog
from django.shortcuts import render, get_object_or_404
# Create your views here.


def BlogView(request, *args, **kwargs):
    posts = Blog.objects.filter(is_published=True).order_by('pub_date')
    
    context = {
        'posts':posts,
    }
    return render(request, 'blog/blog.html', context)

def BlogDetailView(request, slug, pk):
    post = get_object_or_404(Blog, slug=slug, pk=pk)
    context = {
        'post':post,
    }
    return render(request, 'blog/blog-details.html', context)