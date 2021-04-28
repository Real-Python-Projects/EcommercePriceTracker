from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from .models import (Products, PopularBrand, ContactMessage,
                     WishListItem, OrderItem, CustomerOrder,
                     CustomerWishList, Shop, Category)
from User.models import AdminUser, MerchantUser
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import  timezone
from .forms import ProductForm
from django.contrib import messages
from django.core.mail import send_mail

from decouple import config
import json
import requests
from requests.auth import HTTPBasicAuth
from django.contrib.auth.decorators import login_required
from .mpesa_credentials import LipaNaMpesaPassword, MpesaAccessToken

# Create your views here.


def IndexView(request, *args, **kwargs):
    featured_products = Products.objects.filter(is_approved=True)
    new_arrivals = Products.objects.filter(is_approved=True).order_by('-created_at')
    
    content = {
        "featured":featured_products,
        "new_arrivals":new_arrivals,
        "most_viewed":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "hot_sale":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "best_seller":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'index.html', content)

@login_required
def add_to_cart(request, slug, *args, **kwargs):
    product = get_object_or_404(Products, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(user=request.user,
                                                          product=product,
                                                          is_ordered=False)
    order_qs = CustomerOrder.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity has been updated")
            return redirect("products:product-detail", slug=slug)
        else:
            order.products.add(order_item)
            messages.info(request, "product has been added to the cart")
            return redirect("products:product-detail", slug=slug)
    else:
        order = CustomerOrder.objects.create(user=request.user)
        order.products.add(order_item)
        messages.info(request, "Item has been added")
        return redirect("products:product-detail", slug=slug)

@login_required
def remove_from_cart(request, slug, *args, **kwargs):
    product = get_object_or_404(Products, slug=slug)
    order_qs = CustomerOrder.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(user=request.user,
                                                  product=product,
                                                  is_ordered=False)[0]
            order.products.remove(order_item)
            messages.info(request, "Item  has been removed")
            return redirect("products:product-detail", slug=slug)
        messages.info(request, "Product not in the cart")
        return redirect("products:product-detail", slug=slug)
    messages.info(request, "You do not have an active order")
    return redirect("products:product-detail", slug=slug)


@login_required
def add_to_wishlist(request, slug, *args, **kwargs):
    product = get_object_or_404(Products, slug=slug)
    wishlist_item, created = WishListItem.objects.get_or_create(user=request.user
                                                                ,product=product)
    wishlist_qs = CustomerWishList.objects.filter(user=request.user)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        if wishlist.products.filter(product__slug=product.slug).exists():
            messages.info(request, "Item is already on the wishlist")
            return redirect("products:product-detail", slug=slug)
        else:
            wishlist.products.add(wishlist_item)
            messages.info(request, "Item has been added to the wishlist")
            return redirect("products:product-detail", slug=slug)
        
    else:
        wishlist = CustomerWishList.objects.create(user=request.user)
        wishlist.products.add(wishlist_item)
        messages.info(request, "Item added to the cart")
        return redirect("products:product-detail", slug=slug)
    
@login_required
def remove_from_wishlist(request, slug, *args, **kwargs):
    product = get_object_or_404(Products, slug=slug)
    wishlist_qs = CustomerWishList.objects.filter(user=request.user)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        if wishlist.products.filter(product__slug=product.slug).exists():
            wishlist_item = WishListItem.objects.filter(user=request.user,
                                                  product=product)[0]
            wishlist.products.remove(wishlist_item)
            messages.info(request, "Item  has been removed")
            return redirect("products:product-detail", slug=slug)
        messages.info(request, "Product not in the wishlist")
        return redirect("products:product-detail", slug=slug)
    messages.info(request, "Product not in the wishlist")
    return redirect("products:product-detail", slug=slug)
    
def ProductDetailView(request, slug, *args, **kwargs):
    product = get_object_or_404(Products, slug=slug)
    content = {
        "product":product,
        "brands": PopularBrand.objects.all()
    }
    return render(request, 'product-details.html',content)

@login_required
def ProductCreateView(request, *args, **kwargs):
    form = ProductForm
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.instance.added_by_merchant = request.user.merchantuser
            form.save()
            messages.success(request, "Item has been added")
            redirect("products:shop")
    context = {
        "form":form,
        "categories":categories
    }
    return render(request, 'product-form.html', context)


def ShopList(request, *args, **kwargs):
    shops = Shop.objects.all()
    new_arrivals = Products.objects.filter(is_approved=True).order_by('-created_at')

    print(request.user.merchantuser.user)
    context = {
        'shops':shops,
        "new_arrivals":new_arrivals,
        "most_viewed":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "hot_sale":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "best_seller":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "popular_brands": PopularBrand.objects.all(),
    }
    return render(request, 'shop-list.html', context)


def ShopProducts(request,slug, *args, **kwargs):
    shop = get_object_or_404(Shop, slug=slug)
    products = shop.shop_products()
    
    context = {
        'shop':shop,
        'products':products,
    }
    return render(request, 'shop-products.html', context)
    


def ContactView(request, *args, **kwargs):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        print(name)
                            
        send_mail(subject, message, email, ["retechstoreke@gmail.com"], fail_silently=True)
        messages.success(request, "Message Sent")
        form_db = ContactMessage(name=name,
                                    email=email,
                                    phone=phone,
                                    subject=subject,
                                    message=message)
        form_db.save()               
        return HttpResponseRedirect(reverse('products:contact'))
    
    context = {
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'contact-us.html', context)

def CartView(request, *args, **kwargs):
    cart_items = CustomerOrder.objects.get(user=request.user, is_ordered=False)
    
    context = {
        "cart_items": cart_items,
        "popular_brands": PopularBrand.objects.all() or None
    }
    return render(request, 'cart.html', context)

def getAccessToken(request):
    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    
    return HttpResponse(validated_mpesa_access_token)

def CheckoutView(request, *args, **kwargs):
    cart_items = CustomerOrder.objects.get(user=request.user, is_ordered=False)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST['email']
        country = request.POST['country']
        street_address = request.POST['street_address']
        street_address2 = request.POST['street_address2']
        county = request.POST['county']
        town = request.POST['town']
        postcode = request.POST['post_code']
        direct_bank_transfer = request.POST['direct_bank_transfer']
        lipa_na_mpesa = request.POST['lipa_na_mpesa']
        paypal = request.POST['paypal']
        terms = request.POST['terms']
        
        
        if lipa_na_mpesa == 'True':
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization":"Bearer %s" % access_token}
            request = {
                "BusinessShortCode": LipaNaMpesaPassword.business_short_code,
                "Password":LipaNaMpesaPassword.decode_password,
                "Timestamp":LipaNaMpesaPassword.lipa_time,
                "TransactionType":"CustomerPayBillOnline",
                "Amount":"5",
                "PartyA":"254712860997",
                "PartyB":"174379",
                "PhoneNumber":"254712860997",
                "CallBackURL":"https/retechstore.pythonanywhere.com/c2b/confirmation/",
                "AccountReference":"GiftWasHere",
                "TransactionDesc":"myhealth test"
                    }
            response = requests.post(api_url, json=request, headers=headers)
            print(response)
            return HttpResponse('success')
        
        
        
        
        
    
    context = {
        "cart_items": cart_items,
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'checkout.html', context)

def AboutUsView(request, *args, **kwargs):
    return render(request, 'about-us.html', {})


def MyAccountView(request, *args, **kwargs):
    context = {
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'my-account.html', context)

def SpecsCompareView(request, *args, **kwargs):
    context = {
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'compare.html', context)
    
                    