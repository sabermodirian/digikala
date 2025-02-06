from django.urls import path
#from . import views
from .views import product_list_view, product_single_view
app_name = 'products'



urlpatterns = [
    
    path('', product_list_view, name='product_list_view'),
    path('<int:product_id>/',product_single_view, name='product_single_view'),
]



""" # products/urls.py (نسخه اصلاح شده)
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='product_list'),  # مسیر اصلی
    path('<int:product_id>/', views.product_view, name='product_detail'),  # این خط جدید """