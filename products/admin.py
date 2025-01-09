from django.contrib import admin
from .models import Product,Category,Product_Price,ProductOptions,Image,Comment,Question,Answer


# class ProductPriceInline(admin.TabularInline):
#     model = Product_Price
    
# class ProductOptionInline(admin.TabularInline):
#     model = ProductOptions
    
# class ProductCommentInline(admin.TabularInline):
#     model = Comment


# class ProductAnswerInline(admin.TabularInline):
#     model = Answer


class ProductImageInline(admin.TabularInline):
    """
    A custom inline admin interface for the Image model.

    This class allows multiple Image instances to be displayed and edited in a table format.
    """
    model = Image
    
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'name','en_name', 'category')
    list_filter = ['category']
    search_fields = ('name','en_name','description')
    
    inlines = [ProductImageInline]
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','slug','parent')    
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('id',)
    
    fieldsets = (
        ("Details", {
            "fields": ("name","slug","parent"
                       ,"description"),}),
                
        ("Image", {
            "fields": ("icon","image"),
        })    
        
    )
    