from django.shortcuts import render, redirect , reverse # redirect رو import کن
from accounts.forms import UserLoginForm , UserRegisterForm  # noqa: F401
from django.contrib.auth import  login , logout
from products.models import Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.views import LoginView 


# Create your views here.

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

# 

@login_required()
def user_comments_view(request):   
        qr_cmmnts = Comment.objects.filter(user=request.user)
        return render(request,
        
         'accounts/user_comments.html',
        {
            'Context_USRcmmnts' : qr_cmmnts
        }
        )
   

