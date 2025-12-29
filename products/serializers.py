from rest_framework import serializers
from .models import Product , Comment  
# from django.contrib.auth.models import User  
from django.contrib.auth import get_user_model

User = get_user_model() # این خط خودش میفهمه یوزر الان کیه (accounts.User)


class CommentSerializer(serializers.Serializer):  
    """ serializer برای نمایش کامنت ها استفاده میشه از این کلاس """
      # این فیلدها رو فقط برای نمایش می‌ذاریم (Read Only)
    id = serializers.IntegerField(read_only=True)
    
    # فیلدهای ورودی
    title = serializers.CharField(max_length=150)
    text = serializers.CharField()
    rate = serializers.IntegerField()
    
    # 👇 این فیلد توی مدل نیست، پس فقط نمایشی یا برای اعتبارسنجیه
    # اگر توی دیتابیس فیلد user_email نداری، موقع save باید حذفش کنیم
    user_email = serializers.EmailField(required=False)   

    # 👇 تعریف صحیح فیلدهای رابطه‌ای
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True
    )
  
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True
    )

    # ⚠️ مهم: چون از ModelSerializer استفاده نکردی، باید خودت تابع create رو بنویسی!
    # وگرنه موقع save ارور میده که "من نمی‌دونم چطوری ذخیره کنم"
    def create(self, validated_data):
        # چون فیلد user_email توی مدل Comment وجود نداره، از دیکشنری می‌کشیمش بیرون
        # که موقع ساخت آبجکت ارور نده.
        validated_data.pop('user_email', None)
        
        # حالا کامنت رو می‌سازیم
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # برای آپدیت هم باید دستی بنویسی (اگر نیاز داری)
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.product = validated_data.get('product', instance.product)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance




''' این کلاس برای نمایش کامنت ها استفاده میشه از این کلاس بطریق مدلسریالایزر
    برای ساخت کامنتها استفاده میشه از این کلاس 
 '''
class CommentModelSerializer(serializers.ModelSerializer):
    # این خط رو اینجا اضافه کن. 
    # source='user.email' یعنی برو از توی یوزرِ این کامنت، ایمیلش رو بردار بیار! (جادوی جنگو)
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Comment
        # نکته: وقتی فیلد اختصاصی بالا تعریف می‌کنی، خودکار به __all__ اضافه میشه
        fields = '__all__' 
        # یا اگه خواستی دستی لیست بدی:
        # fields = ['id', 'title', 'text', 'rate', 'user', 'product', 'user_email']
        # 👇 این خط جادویی رو اضافه کن:
        # یعنی: «آقای سریالایزر، گیر نده که اینا توی ورودی باشن، خودم حواسم هست»
        read_only_fields = ['user', 'product']

    
    def create(self, validated_data):
        # چون فیلد user_email توی مدل Comment وجود نداره، از دیکشنری می‌کشیمش بیرون
        # که موقع ساخت آبجکت ارور نده.
        validated_data.pop('user_email', None)
        
        # حالا کامنت رو می‌سازیم
        return Comment.objects.create(**validated_data)

    def validate(self, attrs):
        # --- بخش اول: منطق بررسی Rate ---
        # نکته: بهتره با .get بگیری که اگر rate توی درخواست نبود، ارور KeyError نگیری
        rate = attrs.get('rate')
        if rate is not None and rate > 5:
            raise serializers.ValidationError({"rate": "Rate must be between 1 and 5"})

        # --- بخش دوم: اون ارور خاص که خواسته بودی ---
        # ⚠️ هشدار: این خط پایین باعث میشه هیچوقت داده ذخیره نشه!
        # چون داری دستی ارور raise می‌کنی. اگر این برای تست هست، اوکیه.
        # اگر شرط خاصی داره، باید بذاریش توی if
        
        # raise serializers.ValidationError({"message error": "oh no expected result"})

        # اگر اون خط بالا (raise) اجرا بشه، کد اینجا قطع میشه و به خط‌های پایین نمیرسه.
        # پس اگر میخوای کد کار کنه، اون raise دوم رو باید شرطی کنی یا برای تست فعالش کنی.

        return attrs

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

    