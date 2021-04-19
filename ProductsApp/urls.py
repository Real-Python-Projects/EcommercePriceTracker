from django.urls import path
from .views import (IndexView, ContactView, MyAccountView,
                    CheckoutView, CartView, ProductDetailView,
                    Shop)

app_name="products"

urlpatterns = [
    path("", IndexView, name="index"),
    path('product-detail/', ProductDetailView, name="product-detail"),
    path('shop/', Shop, name="shop"),
    path("checkout/", CheckoutView, name="checkout"),
    path("cart/", CartView, name="cart"),
    path("contact", ContactView, name='contact'),
    path('account/<str:user>/', MyAccountView, name="my-account"),
]
