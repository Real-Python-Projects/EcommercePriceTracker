from .models import Category, CustomerOrder

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