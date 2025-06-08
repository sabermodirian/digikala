from django.urls import path
#from . import views
from .views import product_list_view, product_detail_view


app_name = 'products'


"""
تعریف مسیرهای URL برای اپلیکیشن محصولات (Products)

این آرایه شامل مسیرهایی است که برای نمایش لیست محصولات و جزئیات محصول خاص استفاده می‌شوند.

مسیرهای تعریف شده:
1. '/' : نمایش لیست کلی محصولات
2. '/category/<int:category_id>/' : نمایش لیست محصولات براساس دسته‌بندی خاص
3. '/<int:product_id>/' : نمایش جزئیات یک محصول خاص

هر مسیر به یک تابع ویو مشخص ارجاع داده شده و نام مسیرها برای دسترسی آسان‌تر در قالب‌ها و کد استفاده می‌شود.
"""

urlpatterns = [

    # مسیر اصلی: لیست کلی محصولات
    # Main route: general product list

    path('', product_list_view, name='product_list'),

    # مسیر لیست محصولات براساس دسته‌بندی
    # Route for product list filtered by category

    path('category/<int:category_id>/', product_list_view, name='product_list'),

    # مسیر جزئیات یک محصول خاص
    # Route for details of a specific product
    path('<int:product_id>/',product_detail_view, name='product_single_view'),

    # path(, product_detail_view, name='product_detail_view'),
]   
#  حالا به انگلیسی:
"""

URL patterns for the Products app

This list of URL patterns defines routes for displaying the list of products as well as the details of individual products.

Defined routes:
1. '/' : Displays a general list of products
2. '/category/<int:category_id>/' : Displays a filtered list of products based on a specific category
3. '/<int:product_id>/' : Displays details of a specific product

Each route is associated with a specific view function, and route names are used for easier access in templates and code.


"""



"""  
( نسخه اصلاح شده ی  این مدل آدرسدهی در بالا تنظیم شده استه)
# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='product_list'),  # مسیر اصلی
    path('<int:product_id>/', views.product_view, name='product_detail')]  # این خط جدید 
    
"""    