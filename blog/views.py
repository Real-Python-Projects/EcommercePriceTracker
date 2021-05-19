from django.shortcuts import render, reverse
from .models import Blog, BlogMedia, Comments
from ProductsApp.models import PopularBrand, Tags
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def BlogView(request, *args, **kwargs):
    blogs = Blog.objects.filter(is_published=True).order_by('pub_date')
    
    query = request.GET.get('blog_search', None)
    if query is not None:
        blogs = Blog.objects.filter(Q(title__icontains=query))
    
    context = {
        'blogs':blogs,
        'recent':Blog.objects.filter(is_published=True).order_by("-added_date")[:3],
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'blog/blog.html', context)

def BlogDetailView(request, slug, pk,*args, **kwargs):
    post = get_object_or_404(Blog, slug=slug, pk=pk)
    blog_media = BlogMedia.objects.filter(post=post)
    comments = Comments.objects.filter(post=post)
             
    context = {
        'recent':Blog.objects.filter(is_published=True).order_by("-added_date")[:3],
        'post':post,
        'blog_media':blog_media,
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'blog/blog-details.html', context)

def BlogCreateView(request, *args, **kwargs):
    
    return render(request, 'blog-create.html', {})


@login_required
def add_comment(request, slug, pk, *args, **kwargs):
    post = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        content = request.POST['content']
        
        if content == "":
            messages.error(request, "Field can not be left blank")
            return HttpResponseRedirect(reverse('blog:blog-detail', kwargs={'slug':post.slug, 'pk':post.pk}))
        
        comment_model = Comments(
            post=post,
            user=request.user,
            content=content,
        )
        comment_model.save()
        return HttpResponseRedirect(reverse('blog:blog-detail', kwargs={'slug':post.slug, 'pk':post.pk}))