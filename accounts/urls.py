from django.urls import path  # noqa: F401
#from . import views
from .views import login_view , MyLogInView , user_register_view ,\
 user_info_view, logout_view, user_comments_view,get_users_list , UserUpdateView  # noqa: F401
# from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [

    # path('login/',login_view, name='login_view'),
    # path('login/',auth_views.LoginView.as_view(template_name='accounts/login_view.html') , name='login_view'),# class base view for loginView
    path('login/',MyLogInView.as_view() , name='login_view'),# class base view for loginView

    path('register/',user_register_view , name="register_view"),
    #  path('profile/',user_info_view , name="user_info_view"),
     path('profile/',UserUpdateView.as_view() , name="user_info_view"),
     path('profile/comments',user_comments_view , name="user_comments_view"),
     path('logout/',logout_view, name='user_logout_view'),
     path('users-list/',get_users_list, name='users_list'),
] 