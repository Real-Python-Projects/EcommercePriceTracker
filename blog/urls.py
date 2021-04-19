from django.urls import path
from .views import BlogView, BlogDetailView

app_name = 'blog'

urlpatterns = [
    path('', BlogView, name="blog"),
    path('<slug>/<int:pk>/', BlogDetailView, name='blog-detail'),
]
