from django.contrib import admin

from .models import Seller


# Register your models here.


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name','slug')
