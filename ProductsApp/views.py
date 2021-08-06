
from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.utils import timezone
from .models import (Products, PopularBrand, ContactMessage,
                     WishListItem, OrderItem, CustomerOrder,
                     CustomerWishList, Shop, Category, MpesaPayment,
                     Category, CompaireItems, Tags, ProductMedia)
from User.models import AdminUser, MerchantUser, StaffUser, Profile, BestCustomerReviews
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
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .mpesa_credentials import LipaNaMpesaPassword, MpesaAccessToken, MpesaC2BCredential


# Create your views here.

def IndexView(request, *args, **kwargs):
    featured_products = Products.objects.filter(is_approved=True)
    new_arrivals = Products.objects.filter(is_approved=True).order_by('-created_at')
    categories = Category.objects.all()
    cus_reviews = BestCustomerReviews.objects.all()
    
    content = { 
        'categories':categories,
        "featured":featured_products,
        "new_arrivals":new_arrivals,
        "most_viewed":Products.objects.filter(is_approved=True).order_by('-view_count'),
        "hot_sale":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "best_seller":Products.objects.filter(is_approved=True).order_by('-created_at'),
        'cus_reviews':cus_reviews,
        "popular_brands": PopularBrand.objects.all(),
        "latest_blog": Blog.objects.filter(is_published=True).order_by("-pub_date")[:5],
        "base_tags": Tags.objects.filter(show_on_index=True)[:5]
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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            order.products.add(order_item)
            messages.info(request, "product has been added to the cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        order = CustomerOrder.objects.create(user=request.user)
        order.products.add(order_item)
        messages.info(request, "Item has been added")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.info(request, "Product not in the cart")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    messages.info(request, "You do not have an active order")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            wishlist.products.add(wishlist_item)
            messages.info(request, "Item has been added to the wishlist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    else:
        wishlist = CustomerWishList.objects.create(user=request.user)
        wishlist.products.add(wishlist_item)
        messages.info(request, "Item added to the cart")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.info(request, "Product not in the wishlist")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    messages.info(request, "Product not in the wishlist")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def ProductDetailView(request, slug, *args, **kwargs):
    product = get_object_or_404(Products, slug=slug)
    
    #code for implementing most viewed
    product.view_count = int(product.view_count)+1
    product.save()

    related_products = Products.objects.filter(category=product.category).exclude(slug=product.slug)[:6]
    
    content = {
        "featured_products":Products.objects.filter(is_approved=True)[:20],
        "product":product,
        "product_media": ProductMedia.objects.filter(product_id=product),
        "related_products":related_products,
        "popular_brands": PopularBrand.objects.all(),
        'tags': Tags.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'product-details.html',content)

def ProductUpdateView(request, slug, pk):
    product = get_object_or_404(Products, id=pk, slug=slug)

    form = ProductForm(request.POST, request.FILES, instance=product)

    if request.method == 'POST' and product.added_by_merchant.user == request.user:
        if form.is_valid:
            form.save()
            form.save_m2m()
            messages.success(request, "Product was updated successfully")
            return HttpResponseRedirect('products:product-detail', product.slug)
        messages.error(request, "Form is invalid")
        return HttpResponseRedirect('products:product-detail', product.slug)
    
    context = {
        'form':form
        }

    return render(request, 'product-form.html',context)
        
@login_required
def ProductCreateView(request, *args, **kwargs):
    form = ProductForm
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        product_images = request.FILES.getlist('product-images')
        
        if form.is_valid():
            form.instance.added_by_merchant = request.user.merchantuser
            form.save()

            for product_image in product_images:
                ProductMedia.objects.create(product=form.instance,
                                            media_content=product_image)
            messages.success(request, "Item has been added")
            redirect("products:shop")
        content = {
            "form":form,
            "categories":categories,
            "popular_brands": PopularBrand.objects.all(),
            "base_tags": Tags.objects.filter(show_on_index=True)[:5],
        }
        messages.error(request, "form is invalid")
        return render(request, 'product-form.html', content)
    content = {
        "form":form,
        "categories":categories,
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'product-form.html', content)


def ShopList(request, *args, **kwargs):
    shops = Shop.objects.all()
    new_arrivals = Products.objects.filter(is_approved=True).order_by('-created_at')

    content = {
        'shops':shops,
        "new_arrivals":new_arrivals,
        "most_viewed":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "hot_sale":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "best_seller":Products.objects.filter(is_approved=True).order_by('-created_at'),
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'shop-list.html', content)


def ShopProducts(request,slug, *args, **kwargs):
    shop = get_object_or_404(Shop, slug=slug)
    products = shop.shop_products().order_by('view_count')
    
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    content = {
        'shop':shop,
        'products':page_obj,
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'shop-products.html', content)
    


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
    
    content = {
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'contact-us.html', content)

def CartView(request, *args, **kwargs):
    cart_items = CustomerOrder.objects.get(user=request.user, is_ordered=False)
    
    content = {
        "cart_items": cart_items,
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'cart.html', content)

@login_required
def WishListView(request, *args, **kwargs):
    wishlist_items = get_object_or_404(CustomerWishList, user=request.user)
    
    content = {
        'wishlist_items':wishlist_items,
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5]
        
    }
    return render(request, 'wishlist.html', content)

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
        
    content = {
        "cart_items": cart_items,
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'checkout.html', content)


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
    
    content = {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    return JsonResponse(dict(content))

@csrf_exempt
def confirmation(request):   
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    order = CustomerOrder.objects.get(user=request.user)
    
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
    order.is_ordered=True
    order.save()
    
    content = {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    
    return JsonResponse(dict(content))

def AboutUsView(request, *args, **kwargs):
    staffs = StaffUser.objects.filter(list_on_about=True)
    cus_reviews = BestCustomerReviews.objects.all()

    content = {
        "staffs":staffs,
        'cus_reviews':cus_reviews,
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'about-us.html', content)

def CategoryListView(request, slug, *args, **kwargs):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    
    content = {
        'category':category,    
        'categories':categories,
        'products':category.category_objects(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5]
    }
    return render(request, 'category-objects.html', content)


@login_required
def CompaireView(request, *args, **kwargs):
    compaire_items = CompaireItems.objects.get(user=request.user)    
    
    content = {
        'compare_items':compaire_items.products.all(),
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5],
    }
    return render(request, 'compare.html', content)
    

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

@login_required
def MyAccountView(request, *args, **kwargs):
    
    content = {
        "profile":get_object_or_404(Profile, user=request.user),
        "popular_brands": PopularBrand.objects.all(),
        "base_tags": Tags.objects.filter(show_on_index=True)[:5]
    }
    return render(request, 'my-account.html', content)
    
 
def MainSearch(request, *args, **kwargs):    
    query = request.GET.get('product_search', None)
      
    if query is not None:
        products = Products.objects.filter(Q(product_name__icontains=query)|
                                        Q(slug__icontains=query)).order_by('view_count')
        
        paginator = Paginator(products, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)  
        
        content = {
            'query':query,
            'products':page_obj,
            "popular_brands": PopularBrand.objects.all(),
            "base_tags": Tags.objects.filter(show_on_index=True)[:5],
        }
        return render(request,'search-results.html', content)
    
def TagView(request, slug, *args, **kwargs):
    tag = get_object_or_404(Tags, slug=slug)
    
    products = Products.objects.filter(tags=tag)
    
    content = {
        'query':tag,
        'products':products,
        "base_tags": Tags.objects.filter(show_on_index=True)[:5]
    }
    return render(request, 'search-results.html', content)