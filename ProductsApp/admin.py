from django.contrib import admin
from .models import (Categories, SubCategories, Shop,models,
                     Products, ProductDetails, ProductMedia,
                     ShopPrice, ProductTransaction, ProductAbout,
                     ProductTags, ProductQuestions, 
                     ProductReviews, ProductReviewVoting, 
                     ProductVarientItems, CustomerOrders,
                     OrderDeliveryStatus)
# Register your models here.

class SubCategoryInline(admin.TabularInline):
    model = SubCategories
    
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    
admin.site.register(Categories, CategoryAdmin)
admin.site.register(Products)