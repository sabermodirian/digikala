from django.shortcuts import render, redirect , reverse # redirect رو import کن
from accounts.forms import UserLoginForm , UserRegisterForm , MyAuthenticationForm # noqa: F401
from django.contrib.auth import  login , logout
from products.models import Comment
from .models  import User
from django.contrib.auth.decorators import login_required , permission_required  # noqa: F401
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden  # noqa: F401
from django.views.generic import ListView , DetailView , CreateView,\
    UpdateView , DeleteView  # noqa: F401

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.

class MyLogInView(LoginView):
    template_name = 'accounts/login_view.html' #class base view
    authentication_form = MyAuthenticationForm

class UserUpdateView(LoginRequiredMixin,UpdateView):#cbv for update User Account 
    model = User
    fields = [ 'first_name' , 'last_name' ,'mobile']
    queryset = User.objects.all()
    template_name = 'accounts/user_info.html'
    success_url = reverse_lazy('accounts:user_info')    
    login_url = reverse_lazy("accounts:login_view")  # اختیاری، اگر مسیر login خاصی داری


    def get_object(self, queryset=None):
         """  
        Return the object the view is displaying.
         این متد برای مدیریت کاربران است و بجای اینکه آبجکت  pk or slug 
       رابه بدهیم و خودش آبجکتش را پیدا کند 
       این متد آورراید شده و آبجکت مورد نظر را از کاربر میگیرد و استفاده میکند
               """
         return self.request.user


def login_view(request):
    if request.method == 'GET': # 'Get' رو به 'GET' تغییر دادم
        # form = UserLoginForm(request=request) # حالا میتونی request رو پاس بدی
          form = AuthenticationForm()
    else: # یعنی request.method == 'POST'
        # برای حالت POST هم باید request رو پاس بدی و داده‌های POST رو هم به فرم بدی
        # form = UserLoginForm(request.POST, request=request)
        form = AuthenticationForm(data=request.POST , request=request)         
        if form.is_valid():
            # user = form.cleaned_data.get('user') # از .get استفاده کن، امن تره
            login(request = request, user=form.get_user()) # حالا user رو لاگین میکنیم
            my_next = request.GET.get('next' , reverse("accounts:user_info_view"))
            return redirect(my_next)  # به یک مسیر معتبر ریدایرکت کن، مثلاً صفحه اصلی
           
    context = {
        "form":form,
        "cntxt_next":request.GET.get('next' , reverse("accounts:user_info_view"))
    }
    return render(request, 'accounts/login_view.html', context)


def user_register_view(request):
    stts = 200 #  status = valid request
    if request.method == 'GET': # 'Get' رو به 'GET' تغییر دادم
        form = UserRegisterForm() # حالا میتونی request رو پاس بدی
    else: # یعنی request.method == 'POST'
        # برای حالت POST هم باید request رو پاس بدی و داده‌های POST رو هم به فرم بدی
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True) # از .get استفاده کن، امن تره
            login(request = request, user=user) # حالا user رو لاگین میکنیم
            return redirect('accounts:user_info_view')  # به یک مسیر معتبر ریدایرکت کن، مثلاً صفحه اصلی
        else:
            stts = 400 # status = bad request   
    context = {
        "form":form
    }
    return render(request, 'accounts/register_view.html', context , status=stts)

@login_required()
def user_info_view(request):
    return render(request,'accounts/user_info.html',{})


def logout_view(request):
    logout(request)
    return redirect('accounts:user_info_view')

# from products.models import Comment
 

@login_required()
def user_comments_view(request):   
        qr_cmmnts = Comment.objects.filter(user=request.user)
        return render(request,
        
         'accounts/user_comments.html',
        {
            'Context_USRcmmnts' : qr_cmmnts
        }
        )

# @permission_required('accounts.view_users', raise_exception=True)
@login_required()
def get_users_list(request):

    """
    This view renders a page that lists 
    all users in the database if the currently
    logged in user has the permission 'accounts.view_users'.
    If the user does not have this permission, 
    the view returns an HttpResponseForbidden 
    with a message indicating that the user does not have
    permission to view the page.
    """

    # if request.user.has_perm('accounts.view_users'):
    users = User.objects.all()  
    
    return render(request,"accounts/view_all_users.html" ,{
        'users_list' : users
    })
    # else:
    #     return HttpResponseForbidden('You do not have permission to view this page.')




