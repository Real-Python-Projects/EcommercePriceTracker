from django.urls import path
from .views import IndexView, ContactView, MyAccountView

app_name="products"

urlpatterns = [
    path("", IndexView, name="index"),
    path("contact", ContactView, name='contact'),
    path('account/<str:user>/', MyAccountView, name="my-account")
]
