from typing import Any, Dict
from django import forms
from django.contrib.auth import authenticate, login  # noqa: F401
from django.contrib.auth import get_user_model # برای اطمینان از دسترسی به مدل User  # noqa: F401
# مدل User سفارشی شما اینجا import نمیشه، چون get_user_model خودش اون رو برمیگردونه.
# اگر model = User رو در Meta استفاده میکنید، باید مدل User رو import کنید.
# اگر User مدل پیش فرض Django هست، نیازی به import کردن نیست.
# اما چون شما از .models import User استفاده کردید، مطمئن شید که مدل User شما درست import شده.
from .models import User
# فرض می‌کنیم مدل User شما در accounts/models.py هست و به این شکل import میشه:
# from django.contrib.auth import get_user_model
# User = get_user_model()
# یا اگر مدل سفارشی خودتون رو ساختید:
# from .models import User # این خط باید درست باشه اگر مدل User سفارشی هست

class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        widget=forms.EmailInput({"class": "form-control"}),
        required=True
    )

    password = forms.CharField(
        widget=forms.PasswordInput({"class": "form-control"}),
        required=True
    )

    def clean(self) -> Dict[str, Any]:
        clean_data = super().clean()
        email = clean_data.get("email")
        password = clean_data.get("password")

        if email and password:
            # فرض می‌کنیم User Model شما برای لاگین از email استفاده میکنه.
            user = authenticate(self.request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    clean_data['user'] = user
                else:
                    raise forms.ValidationError("حساب کاربری شما فعال نیست.")
            else:
                raise forms.ValidationError('ایمیل یا رمز عبور اشتباه است.')
        else:
            raise forms.ValidationError("لطفاً هم ایمیل و هم رمز عبور را وارد کنید.")
            
        return clean_data


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput({"class":"form-control"}),
        label="کلمه عبور")

    password2 = forms.CharField(
        widget=forms.PasswordInput({"class":"form-control"}),
        label="کلمه عبور تکرار")

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "mobile",
            "password1", # این خط اینجا قرار میگیره
            "password2", # و این خط هم اینجا
        )

    # متد clean باید بیرون از کلاس Meta باشه:
    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        password1 = cleaned_data.pop("password1", None)
        password2 = cleaned_data.pop("password2", None)
        
        if password1 and password2 and password1 != password2:
            # از add_error برای اضافه کردن خطا به فیلد خاص استفاده می‌کنیم
            self.add_error("password2", forms.ValidationError("در ورود پسورد کوشا باشید", code="invalid"))
            # یا اگر می‌خواهید خطا به صورت عمومی نمایش داده شود:
            # raise forms.ValidationError("رمزهای عبور وارد شده مطابقت ندارند.")
            
        # اگر رمز عبورها درست بود، password1 را به cleaned_data اضافه می‌کنیم تا در save استفاده شود
        # اگر password1 و password2 خالی نبودند و با هم مطابقت داشتند
        if password1 and password1 == password2:
            cleaned_data["password"] = password1
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # اینجا باید password رو از cleaned_data بگیریم، نه اینکه دوباره pop کنیم
        password = self.cleaned_data.get("password")
        if password: # اگر password در cleaned_data وجود داشت
            user.set_password(password)
        
        if commit:
            user.save()
            
        return user
