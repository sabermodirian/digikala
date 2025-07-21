from django.contrib import admin
from .models import Product,Category,SellerProductPrice,\
Image,Comment,Question,Answer,ProductOptions,Brand  # noqa: F401

"""
Inline Admin:
قابلیتی در Django Admin برای مدیریت مدل‌های مرتبط به صورت تو در تو
مثلاً نمایش قیمت مرتبط با یک محصول در همان صفحه ویرایش محصول
در صورتی که می‌خواهید کاربران در همان ویرایش محصولات، به صورت جداگانه یک محصول را تغییر دهند.

Table Format:
نمایش اطلاعات به صورت سطر و ستون
امکان مرتب‌سازی، جستجو و فیلتر کردن داده‌ها

کاربرد عملی:
وقتی می‌خواهید والد و فرزند را همزمان در یک صفحه مدیریت کنید
کاهش مراحل کار و افزایش سرعت عملیات

"""
class ProductPriceInline(admin.TabularInline):
    model = SellerProductPrice
    extra = 1
    
class ProductOptionInline(admin.TabularInline):
    """
    A custom inline admin interface for the ProductOptions model.

    This class allows multiple ProductOptions instances to be displayed and edited in a table format.
    """
    model = ProductOptions
    extra = 1
    
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
    extra = 1
    
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'name','en_name', 'category')
    list_filter = ['category']
    search_fields = ('name','en_name','description')
    
    inlines = [ProductImageInline,ProductOptionInline,
               ProductPriceInline]
    

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
    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'en_name','slug')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','user_email','Product' ,'title', 'rate')
    
    search_fields = ('product_id', 'user', 'text')


# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     pass
