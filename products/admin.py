from django.contrib import admin
from .models import Product,Category,Product_Price,ProductOptions,Image,Comment,Question,Answer

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','slug','parent')    
    list_filter = ('category',)
    search_fields = ('name', 'description')