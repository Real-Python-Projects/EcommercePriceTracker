from .models import Category, CustomerOrder
from User.models import EmailSubscibers
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def category_context_preprocessor(request):
    context = {
        'categories':Category.objects.all()
    }
    return context

def user_cart_items(request):
    if request.user.is_authenticated:
        user_order = CustomerOrder.objects.filter(user=request.user, is_ordered=False)
        if user_order.exists():
            user_order_items = user_order[0].products.all()
            return {
                'prep_cart_items':user_order_items
            }
    user_order_items = False
    return {
            'prep_cart_items':user_order_items
        }
    
def EmailSub(request, *args, **kwargs):
    if request.method == 'POST':
        sub_email = request.POST['sub_email']
        
        email_qs = EmailSubscibers.objects.filter(email=sub_email)
        
        if email_qs.exists():
            messages.error(request, 'Email already exists')
            return HttpResponseRedirect(reverse('products:index'))
        
        subscribers = EmailSubscibers(
            email = sub_email
        )
        subscribers.save()
        messages.success(request, "Thanyou for subscribing")

    return HttpResponseRedirect(reverse('products:index'))