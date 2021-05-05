
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from .models import (Products, PopularBrand, ContactMessage,
                     WishListItem, OrderItem, CustomerOrder,
                     CustomerWishList, Shop, Category, MpesaPayment,
                     Category, CompaireItems)
from User.models import AdminUser, MerchantUser, StaffUser, Profile
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import  timezone
from .forms import ProductForm
from django.contrib import messages
from django.core.mail import send_mail

from blog.models import Blog
from decouple import config
from django.db.models import Q
import json
import requests
from requests.auth import HTTPBasicAuth

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .mpesa_credentials import LipaNaMpesaPassword, MpesaAccessToken, MpesaC2BCredential


# Create your views here.

def IndexView(request, *args, **kwargs):
    featured_products = Products.objects.filter(is_approved=True)
    new_arrivals = Products.objects.filter(is_approved=True).order_by('-created_at')
    categories = Category.objects.all()
    
    content = {
        'categories':categories,
        "featured":featured_products,
        "new_arrivals":new_arrivals,
        "most_viewed":Products.objects.filter(is_approved=True).order_by('-view_count'),
        "hot_sale":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "best_seller":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "popular_brands": PopularBrand.objects.all(),
        "latest_blog": Blog.objects.filter(is_published=True).order_by("-pub_date")[:5],
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
    
    #code for implementing most viewed
    product.view_count = int(product.view_count)+1
    product.save()
    
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

@login_required
def WishListView(request, *args, **kwargs):
    wishlist_items = get_object_or_404(CustomerWishList, user=request.user)
    
    context = {
        'wishlist_items':wishlist_items,
        "popular_brands": PopularBrand.objects.all() or None
        
    }
    return render(request, 'wishlist.html', context)

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
        email = request.POST.get('email')
        country = request.POST.get('country')
        street_address = request.POST.get('street_address')
        street_address2 = request.POST.get('street_address2')
        county = request.POST.get('county')
        town = request.POST.get('town')
        postcode = request.POST.get('post_code')
        payment_method = request.POST.get('paymentmethod')
        lipa_na_mpesa_phone = request.POST.get('mpesa_phone')
        terms = request.POST.get('terms')
        
        print(payment_method)
        
        if payment_method == 'mpesa':
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization":"Bearer %s" % access_token}
            request = {
                "BusinessShortCode": LipaNaMpesaPassword.business_short_code,
                "Password":LipaNaMpesaPassword.decode_password,
                "Timestamp":LipaNaMpesaPassword.lipa_time,
                "TransactionType":"CustomerPayBillOnline",
                "Amount":"5",
                "PartyA":f"{lipa_na_mpesa_phone}",
                "PartyB":"174379",
                "PhoneNumber":f"{lipa_na_mpesa_phone}",
                "CallBackURL":"https://retechstore.pythonanywhere.com/c2b/confirmation/",
                "AccountReference":"GiftWasHere",
                "TransactionDesc":"myhealth test"
                    }
            response = requests.post(api_url, json=request, headers=headers)
            return HttpResponse('success')
        
    context = {
        "cart_items": cart_items,
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'checkout.html', context)


#register confirmation and validation url with safaricom

@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipaNaMpesaPassword.test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://93c0351429ab.ngrok.io/c2b/confirmation/",
               "ValidationURL": "https://93c0351429ab.ngrok.io/c2b/validation/"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

#simulate transaction

@csrf_exempt
def simulate_transaction(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = { "ShortCode":LipaNaMpesaPassword.test_c2b_shortcode,
                "CommandID":"CustomerPayBillOnline",
                "Amount":"500",
                "Msisdn":"254708374149",
                "BillRefNumber":LipaNaMpesaPassword.business_short_code}
  
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse(response.text)


#capture the mpesa calls
@csrf_exempt
def call_back(request):
    pass

@csrf_exempt
def validation(request):
    data = json.loads(request.body)
    file = open('validate.json','a')
    file.write(json.dumps(data))
    file.close()
    
    context = {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    return JsonResponse(dict(context))

@csrf_exempt
def confirmation(request):   
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    
    payment = MpesaPayment (
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType']
    )
    payment.save()
    context = {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    
    return JsonResponse(dict(context))

def AboutUsView(request, *args, **kwargs):
    staffs = StaffUser.objects.filter(list_on_about=True)
    context = {
        "staffs":staffs
    }
    return render(request, 'about-us.html', context)

def SerchView(request, *args, **kwargs):
    pass


def CategoryListView(request, slug, *args, **kwargs):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    

        
    
    context = {
        'category':category,    
        'categories':categories,
        'products':category.category_objects()
    }
    return render(request, 'category-objects.html', context)


@login_required
def CompaireView(request, *args, **kwargs):
    compaire_items = CompaireItems.objects.get(user=request.user)    
    
    context = {
        'compare_items':compaire_items.products.all(),
        "popular_brands": PopularBrand.objects.all(),
    }
    return render(request, 'compare.html', context)
    

@login_required
def add_to_compaire(request, slug, *args, **kwargs):
    product = get_object_or_404(Products, slug=slug)
    compaire_qs = CompaireItems.objects.filter(user=request.user)
    compare_item = Products.objects.get(slug=slug)
    if compaire_qs.exists():
        compaire = compaire_qs[0]
        
        clicked_item = compaire.products.filter(slug=product.slug)
        
        if clicked_item.exists():
            messages.info(request, "Item is already on the compare items")
            return redirect('products:compare', user=request.user)
        compaire.products.add(compare_item)
        return redirect('products:compare', user=request.user)
    
    
    compare = CompaireItems.objects.create(user=request.user)
    compare.products.add(compare_item)
    messages.success(request, "item was added to compaire")
    redirect('products:compare', user=request.user)
    
def MyAccountView(request, *args, **kwargs):
    
    context = {
        "profile":get_object_or_404(Profile, user=request.user),
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'my-account.html', context)
    
 
def MainSearch(request, *args, **kwargs):    
    query = request.GET.get('product_search', None)
        
    if query is not None:
        products = Products.objects.filter(Q(product_name__icontains=query)|
                                        Q(slug__icontains=query))
        context = {
            'query':query,
            'products':products
        }
        return render(request,'search-results.html', context)