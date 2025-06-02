from django.urls import path
from django.conf.urls import include


appname = 'sellers'

urlpatterns = [

    path('', include('sellers.urls')),    
    
]