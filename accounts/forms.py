from typing import Any, Dict
from django import forms
from django.contrib.auth import authenticate, login  # noqa: F401
from django.contrib.auth import get_user_model # برای اطمینان از دسترسی به مدل User  # noqa: F401
from .models import User

# # برای استفاده از مدل User سفارشی‌تون

class UserLoginForm(forms.Form):
    # 1. اشتباه تایپی __init__ رو درست کن (دو آندرلاین قبل و بعد)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) # request رو از kwargs برمیداره
        super().__init__(*args, **kwargs) # بقیه پارامترها رو به والد میفرسته

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
        
        # 2. از 'email' استفاده کن چون فیلد فرم email هست نه username
        email = clean_data.get("email") # بهتره از .get استفاده کنی تا خطا نده اگه فیلد نباشه
        password = clean_data.get("password")

        # اگر هر دو فیلد email و password پر شده باشن
        if email and password:
            # 3. ترتیب پارامترهای authenticate:
            # authenticate معمولا username= و password= میگیره.
            # اگر User Model شما با email لاگین میکنه (و email رو به عنوان USERNAME_FIELD تعریف کرده)،
            # باید اینجا email رو به جای username پاس بدی.
            # من فرض میکنم User Model شما برای لاگین از email استفاده میکنه.
            # اگر username رو هم داره و با اون لاگین میکنه، باید فیلد username رو به فرمت اضافه کنی.

            # اگر با ایمیل لاگین میکنی:
            user = authenticate(self.request, email=email, password=password)
            # اگر با username لاگین میکنی و فیلد username توی فرمت نیست:
            # user = authenticate(self.request, username=email, password=password)
            # یا اگر فیلد username رو به فرم اضافه کردی:
            # user = authenticate(self.request, username=username, password=password)


            if user is not None:
                if user.is_active: # چک کن که کاربر فعال باشه
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

    password2 =forms.CharField(
        widget=forms.PasswordInput({"class":"form-control"}), 
        label="کلمه عبور تکرار")
    

    class Meta:
     model = User
     fields = {
        "first_name"
        ,"last_name"
        ,"email"
        ,"mobile"
        ,"password"
     }

    def clean(self)-> Dict[str,Any]:
        cleaned_data = super().clean()
        password1=cleaned_data.pop("password1",None)
        password2=cleaned_data.pop("password2",None)
        if password1 != password2 :
            self.add_error("password2" , forms.ValidationError(
                "در ورود پسورد کوشا باشید", code="invalid"))
        cleaned_data.setdefault("password",password1)
        return cleaned_data
    
    def save(self , commit) -> Any: 
        user = super.save(commit)
        user.setpassword(self.changed_data("password1"))
        if commit:
            user.save()
        else:
            return user




