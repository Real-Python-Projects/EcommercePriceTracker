from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from User.models import AdminUser, MerchantUser
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail


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


def ContactView(request, *args, **kwargs):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.post.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name == "":
            messages.error(request, "name is required")
            if phone == "":
                message.error(request, "Phone is required")
                if email == "":
                    messages.error(request, "Email is required")
                    if subject == "":
                        messages.error(request, "subject is required")
                        if message == "":
                            messages.error(request, "message is required")
                            
                            send_mail(subject, message, email, ["retechstoreke@gmail.com"], fail_silently=True)
                            form_db = ContactMessage(name=name,
                                                     email=email,
                                                     phone=phone,
                                                     subject=subject,
                                                     message=message)
                            form_db.save()
                            
                            
        return HttpResponseRedirect(reverse('products:contact-page'))
    
    content = {
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'contact-us.html', {})
                    