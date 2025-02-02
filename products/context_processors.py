from .models import Category

def categories_navbar(request):
    categories = Category.objects.all()
    return {
        'categories_navbr':categories
        }