from django.urls import path
from .views import BlogView, BlogDetailView

app_name = 'blog'

urlpatterns = [
    path('', BlogView, name="blog"),
    path('detail/', BlogDetailView, name='blog-detail'),
]
