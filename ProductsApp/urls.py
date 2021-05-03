from django.urls import path
from .views import (IndexView, ContactView, MyAccountView,
                    CheckoutView, CartView, ProductDetailView, ShopList, ShopProducts,
                    add_to_wishlist,remove_from_wishlist, remove_from_cart,
                    add_to_cart, ProductCreateView, WishListView,
                    AboutUsView, CompaireView, CategoryListView,
                    add_to_compaire)
from .context_processors import EmailSubscibers

app_name="products"

urlpatterns = [
    path("", IndexView, name="index"),
    path('shop/', ShopList, name="shop"),
    path('shop/<slug>/', ShopProducts, name="shop-products"),
    path('shop/merchant/add-product/', ProductCreateView, name="add-product"),
    path('about-us/', AboutUsView, name="about-us"),
    path('compare-specs/<user>/', CompaireView, name="compare"),
    path("cart/", CartView, name="cart"),
    path('product/<slug>/', ProductDetailView, name="product-detail"),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('wishlist/<user>/', WishListView, name='wishlist'),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path("add-to-wishlist/<slug>/",add_to_wishlist, name="add-to-wishlist"),
    path("remove-fom-wishlist/<slug>/",remove_from_wishlist, name="remove-from-wishlist"),
    path("checkout/", CheckoutView, name="checkout"),
    path("contact", ContactView, name='contact'),
    path('view-product-by-category/<slug>/', CategoryListView, name='category-objects'),
    path('account/<str:user>/', MyAccountView, name="my-account"),
    path('subscribe/email/', EmailSubscibers, name="subscribe"),
    path('compare/<user>/add-to-compare/<slug>/', add_to_compaire, name = 'add-to-compare'),
]
