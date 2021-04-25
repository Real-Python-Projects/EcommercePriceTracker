from django.urls import path
from .views import (IndexView, ContactView, MyAccountView,
                    CheckoutView, CartView, ProductDetailView, ShopList, ShopProducts,
                    add_to_wishlist,remove_from_wishlist, remove_from_cart,
                    add_to_cart, ProductCreateView,
                    AboutUsView, SpecsCompareView)

app_name="products"

urlpatterns = [
    path("", IndexView, name="index"),
    path('shop/', ShopList, name="shop"),
    path('shop/<slug>/', ShopProducts, name="shop-products"),
    path('shop/merchant/add-product/', ProductCreateView, name="add-product"),
    path('about-us/', AboutUsView, name="about-us"),
    path('compare-specs/', SpecsCompareView, name="specs-compare"),
    path('<slug>/', ProductDetailView, name="product-detail"),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path("add-to-wishlist/<slug>/",add_to_wishlist, name="add-to-wishlist"),
    path("remove-fom-wishlist/<slug>/",remove_from_wishlist, name="remove-from-wishlist"),
    path("checkout/", CheckoutView, name="checkout"),
    path("cart/", CartView, name="cart"),
    path("contact", ContactView, name='contact'),
    path('account/<str:user>/', MyAccountView, name="my-account"),
]
