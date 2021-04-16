from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from User.models import AdminUser, MerchantUser

# Create your views here.


def IndexView(request, *args, **kwargs):
    return render(request, 'index.html', {})