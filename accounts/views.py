from django.shortcuts import render
from accounts.forms import UserLoginForm
from django.contrib.auth import authenticate , login  # noqa: F401

# Create your views here.

def login_view(request):
    if request.method == 'Get':
        form = UserLoginForm()

    else:

        form = UserLoginForm(request.POST , request=request)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request = request,user=user)
            return redirect['']  # noqa: F821

    context = {
        "form":form
    }
    return render(request, 'accounts/login_view.html', context)