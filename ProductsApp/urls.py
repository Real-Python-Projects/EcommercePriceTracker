from django.urls import path
from .views import (IndexView, ContactView, MyAccountView,
                    CheckoutView, CartView, ProductDetailView,
                    ShopList, ShopProducts,add_to_wishlist, ProductCreateView)

app_name="products"

urlpatterns = [
    path("", IndexView, name="index"),
    path('shop/', ShopList, name="shop"),
    path('shop/<slug>/', ShopProducts, name="shop-products"),
    path('shop/merchant/add-product/', ProductCreateView, name="add-product"),
    path('<slug>/', ProductDetailView, name="product-detail"),
    path("add-to-wishlist/<slug>/",add_to_wishlist, name="add-to-wishlist"),
    path("checkout/", CheckoutView, name="checkout"),
    path("cart/", CartView, name="cart"),
    path("contact", ContactView, name='contact'),
    path('account/<str:user>/', MyAccountView, name="my-account"),
]
