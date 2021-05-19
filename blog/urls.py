from django.urls import path
from .views import BlogView, BlogDetailView, add_comment

app_name = 'blog'

urlpatterns = [
    path('', BlogView, name="blog"),
    path('<slug>/<int:pk>/', BlogDetailView, name='blog-detail'),
    path('<slug>/<int:pk>/add-comment/', add_comment, name='add-comment'),
]
