from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_rate(value):
    if value > 5:
        raise ValidationError(_("Rate must be between 1 and 5."))

    # --- بخش دوم: اون ارور خاص که خواسته بودی ---
    # ⚠️ هشدار: این خط پایین باعث میشه هیچوقت داده ذخیره نشه!
    # چون داری دستی ارور raise می‌کنی. اگر این برای تست هست، اوکیه.
    # اگر شرط خاصی داره، باید بذاریش توی if
    
    # raise serializers.ValidationError({"message error": "oh no expected result"})

    # اگر اون خط بالا (raise) اجرا بشه، کد اینجا قطع میشه و به خط‌های پایین نمیرسه.
    # پس اگر میخوای کد کار کنه، اون raise دوم رو باید شرطی کنی یا برای تست فعالش کنی.

    # return attrs

    # یا

#  # این فقط مخصوص فیلد rate اجرا میشه
#     def validate_rate(self, value):
#         if value > 5:
#             raise serializers.ValidationError("Rate must be between 1 and 5")
#         return value

#     # این برای بررسی‌های کلی و ترکیبی اجرا میشه
#     def validate(self, attrs):
#         # اینجا میتونی اون منطق دومت رو بنویسی
#         # if some_condition:
#         #     raise serializers.ValidationError(...)
#         return attrs
