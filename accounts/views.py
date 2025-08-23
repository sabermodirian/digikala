from django.shortcuts import render, redirect # redirect رو import کن
from accounts.forms import UserLoginForm
from django.contrib.auth import authenticate , login # این رو هم نگه دار  # noqa: F401

# Create your views here.

def login_view(request):
    if request.method == 'GET': # 'Get' رو به 'GET' تغییر دادم
        form = UserLoginForm(request=request) # حالا میتونی request رو پاس بدی
    else: # یعنی request.method == 'POST'
        # برای حالت POST هم باید request رو پاس بدی و داده‌های POST رو هم به فرم بدی
        form = UserLoginForm(request.POST, request=request)
        if form.is_valid():
            user = form.cleaned_data.get('user') # از .get استفاده کن، امن تره
            login(request = request, user=user) # حالا user رو لاگین میکنیم
            return redirect('/')  # به یک مسیر معتبر ریدایرکت کن، مثلاً صفحه اصلی
           
    context = {
        "form":form
    }
    return render(request, 'accounts/login_view.html', context)
