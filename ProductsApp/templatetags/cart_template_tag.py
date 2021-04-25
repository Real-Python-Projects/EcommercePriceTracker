from django import template
from ProductsApp.models import CustomerOrder

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        user_order = CustomerOrder.objects.filter(user=user, is_ordered=False)
        if user_order.exists():
            return user_order[0].products.count()
        return 0

@register.filter    
def cart_total_order(user):
    if user.is_authenticated:
        user_order = CustomerOrder.objects.filter(user=user, is_ordered=False)
        if user_order.exists():
            return user_order[0].totalorderPrice()
        return 0