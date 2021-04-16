from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from User.models import AdminUser, MerchantUser

# Create your views here.


def IndexView(request, *args, **kwargs):
    featured_products = Products.objects.filter(is_active=True)
    new_arrivals = Products.objects.filter(is_active=True).order_by('-created_at')
    
    content = {
        "featured":featured_products,
        "new_arrivals":new_arrivals,
        "most_viewed":Products.objects.filter(is_active=True).order_by('-created_at'),
        "hot_sale":Products.objects.filter(is_active=True).order_by('-created_at'),
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'index.html', content)


def Shop(request, *args, **kwargs):
    shop = MerchantUser.objects.all()
    
    shop_products = Products.objects.filter(added_by_merchant=shop)
    
    context = {
        'shop_items':shop_products,
    }
    return render(request, 'shop.html', context)