from django.urls import path  # noqa: F401
#from . import views
from .views import login_view  # noqa: F401

app_name = 'accounts'

urlpatterns = [

    path('login/',login_view, name='login_view')
] 