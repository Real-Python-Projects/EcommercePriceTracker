from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from User.models import AdminUser, MerchantUser

# Create your views here.


def IndexView(request, *args, **kwargs):
    return render(request, 'index.html', {})


def Shop(request, *args, **kwargs):
    shop_items = Item.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')
    context = {
        'shop_items':shop_items,
    }
    return render(request, 'shop.html', context)