from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from User.models import AdminUser, MerchantUser

# Create your views here.


def IndexView(request, *args, **kwargs):
    return render(request, 'index.html', {})


def Shop(request, *args, **kwargs):
    shop = MerchantUser.objects.all()
    
    shop_products = Products.objects.filter(added_by_merchant=shop)
    
    context = {
        'shop_items':shop_products,
    }
    return render(request, 'shop.html', context)