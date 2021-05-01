from .models import Category, CustomerOrder
from User.models import EmailSubscibers
from django.shortcuts import redirect
from django.contrib import messages

def category_context_preprocessor(request):
    context = {
        'categories':Category.objects.all()
    }
    return context

def user_cart_items(request, *args, **kwargs):
    if request.user.is_authenticated:
        user_order = CustomerOrder.objects.filter(user=request.user, is_ordered=False)
        if user_order.exists():
            user_order_items = user_order[0].products.all()
            return {
                'prep_cart_items':user_order_items
            }
        return 0
    
def SubscribeEmail(request, *args, **kwargs):
    if request.method == 'POST':
        sub_email = request.POST.get('sub_email')
        
        email_qs = EmailSubscibers.objects.filter(email=sub_email)
        
        if email_qs.exists():
            messages.error(request, 'Email already exists')
            return redirect(request.META['HTTP_REFERER'])   
        
        subscribers = EmailSubscibers(
            email = sub_email
        )
        subscribers.save()
        messages.success(request, "Thanyou for subscribin")
    
    context = {}
    return context