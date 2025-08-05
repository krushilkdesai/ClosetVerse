from .models import Category

def categories_processor(request):
    """Make categories available in all templates"""
    return {
        'categories': Category.objects.all().order_by('name')
    }
