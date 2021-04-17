from django.urls import path
from .views import IndexView, ContactView

app_name="products"

urlpatterns = [
    path("", IndexView, name="index"),
    path("contact", ContactView, name='contact'),
]
