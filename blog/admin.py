from django.contrib import admin
from .models import BlogCategory, Blog, Comments, BlogMedia, Tag
from mptt.admin import DraggableMPTTAdmin
# Register your models here.


# admin.site.register(BlogCategory)


class BlogMediaInLine(admin.TabularInline):
    model = BlogMedia
    extra = 1
    
class BlogCommentInline(admin.TabularInline):
    model = Comments
    extra = 1
    
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogMediaInLine, BlogCommentInline]
    
admin.site.register(Blog, BlogAdmin)

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
admin.site.register(Tag)