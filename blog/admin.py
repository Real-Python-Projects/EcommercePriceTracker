from django.contrib import admin
from .models import BlogCategory, Blog
from mptt.admin import DraggableMPTTAdmin
# Register your models here.


# admin.site.register(BlogCategory)
admin.site.register(Blog)

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_blogs_count', 'related_blogs_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = BlogCategory.objects.add_related_count(
                qs,
                Blog,
                'category',
                'blogs_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = BlogCategory.objects.add_related_count(qs,
                 Blog,
                 'category',
                 'blogs_count',
                 cumulative=False)
        return qs
    
    def related_blogs_count(self, instance):
        return instance.blogs_count
    related_blogs_count.short_description = 'Related blogs (for this specific category)'

    def related_blogs_cumulative_count(self, instance):
        return instance.blogs_cumulative_count
    related_blogs_cumulative_count.short_description = 'Related blogs (in tree)'
    
admin.site.register(BlogCategory, CategoryAdmin)