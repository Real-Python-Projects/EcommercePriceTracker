from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import (Category,Shop,models,Products, ProductDetails, ProductMedia,
                     ShopPrice, ProductTransaction, ProductAbout,ProductQuestions, 
                     ProductReviews, ProductReviewVoting, ProductVarientItems, CustomerOrder,
                     OrderDeliveryStatus, PopularBrand, ContactMessage,
                     CustomerWishList, OrderItem, CompaireItems, Tags,
                     MpesaPayment)

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Products,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Products,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs
    
    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related blogs (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related category (in tree)'
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop)


class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 1 

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductMediaInline]
admin.site.register(Products, ProductAdmin)


admin.site.register(OrderItem)
admin.site.register(CustomerOrder)
admin.site.register(CustomerWishList)

admin.site.register(MpesaPayment)
admin.site.register(PopularBrand)
admin.site.register(ContactMessage)
admin.site.register(CompaireItems)
admin.site.register(Tags)
