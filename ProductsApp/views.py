from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from .models import (Products, PopularBrand, ContactMessage,
                     WishListItem, CustomerWishList, Shop, Category)
from User.models import AdminUser, MerchantUser
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import  timezone
from .forms import ProductForm
from django.contrib import messages
from django.core.mail import send_mail


from django.contrib.auth.decorators import login_required

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
    products = shop.shop_products
    
    print(products)
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

def CheckoutView(request, *args, **kwargs):
    context = {
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'checkout.html', context)

def CartView(request, *args, **kwargs):
    context = {
        "popular_brands": PopularBrand.objects.all()
    }
    return render(request, 'cart.html', context)

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
    
                    