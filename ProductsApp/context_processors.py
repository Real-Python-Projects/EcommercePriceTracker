from .models import Category

def category_context_preprocessor(request):
    context = {
        'categories':Category.objects.all()
    }
    return context