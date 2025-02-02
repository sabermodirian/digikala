from django.urls import path
from . import views

app_name = 'products'



urlpatterns = [
    
    path('', views.index, name='index_view'),
    path('<int:product_id>/', views.product_view, name='product_view'),
]



""" # products/urls.py (نسخه اصلاح شده)
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='product_list'),  # مسیر اصلی
    path('<int:product_id>/', views.product_view, name='product_detail'),  # این خط جدید """