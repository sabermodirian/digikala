# from products.api.v1.models import User
from ...models import Product , Comment , Brand , Category , SellerProductPrice # noqa: F401 #== معادل خط بالا

from rest_framework import serializers

from sellers.api.v1.serializers import SellerSerializer
 
# from django.contrib.auth.models import User  
from django.contrib.auth import get_user_model



User = get_user_model() # این خط خودش میفهمه یوزر الان کیه (accounts.User)

#  class CommentSerializer(serializers.Serializer):  
#    """ serializer برای نمایش کامنت ها استفاده میشه از این کلاس """
#       # این فیلدها رو فقط برای نمایش می‌ذاریم (Read Only)
#     id = serializers.IntegerField(read_only=True)
    
#     # فیلدهای ورودی
#     title = serializers.CharField(max_length=150)
#     text = serializers.CharField()
#     rate = serializers.IntegerField()
    
#     # 👇 این فیلد توی مدل نیست، پس فقط نمایشی یا برای اعتبارسنجیه
#     # اگر توی دیتابیس فیلد user_email نداری، موقع save باید حذفش کنیم
#     user_email = serializers.EmailField(required=False)   

#     # 👇 تعریف صحیح فیلدهای رابطه‌ای
#     product = serializers.PrimaryKeyRelatedField(
#         queryset=Product.objects.all(),
#         required=True
#     )
  
#     user = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         required=True
#     )

#     # ⚠️ مهم: چون از ModelSerializer استفاده نکردی، باید خودت تابع create رو بنویسی!
#     # وگرنه موقع save ارور میده که "من نمی‌دونم چطوری ذخیره کنم"
#     def create(self, validated_data):
#         # چون فیلد user_email توی مدل Comment وجود نداره، از دیکشنری می‌کشیمش بیرون
#         # که موقع ساخت آبجکت ارور نده.
#         validated_data.pop('user_email', None)
        
#         # حالا کامنت رو می‌سازیم
#         return Comment.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         # برای آپدیت هم باید دستی بنویسی (اگر نیاز داری)
#         instance.title = validated_data.get('title', instance.title)
#         instance.text = validated_data.get('text', instance.text)
#         instance.rate = validated_data.get('rate', instance.rate)
#         instance.product = validated_data.get('product', instance.product)
#         instance.user = validated_data.get('user', instance.user)
#         instance.save()
#         return instance


class CommentModelSerializer(serializers.ModelSerializer):
    '''
    این کلاس برای نمایش کامنت ها استفاده میشه از این کلاس بطریق مدلسریالایزر
    برای ساخت کامنتها استفاده میشه
    '''
    # این 👇 خط رو اینجا اضافه کن. 
    # source='user.email' یعنی برو از توی یوزرِ این کامنت، ایمیلش رو بردار بیار! (جادوی جنگو)
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Comment
        # نکته: وقتی فیلد اختصاصی بالا تعریف می‌کنی، خودکار به __all__ اضافه میشه
        # fields = '__all__' 
        # یا اگه خواستی دستی لیست بدی:
        fields = ['id',
         'title',
          'text',
          'rate',
           'user',
           'product',
            'user_email']
        # 👇 این خط جادویی رو اضافه کن:
        # یعنی: «آقای سریالایزر، به من تورو خدا گیر.نده که اینا توی ورودی باشن، خودم حواسم هست»
        read_only_fields = ['user', 'product']

    
    def create(self, validated_data):
        # چون فیلد user_email توی مدل Comment وجود نداره، از دیکشنری می‌کشیمش بیرون
        # که موقع ساخت آبجکت ارور نده.
        validated_data.pop('user_email', None)
        
        # حالا کامنت رو می‌سازیم
        return Comment.objects.create(**validated_data)


class BrandSerializer(serializers.ModelSerializer):


    class Meta:
        model = Brand
        fields = "__all__" 


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__" 

class ProductPriceSerializer(serializers.ModelSerializer):

    seller_details = SellerSerializer(source='seller', read_only=True)
    ''' با استفاده از خط بالا کل اطلاعات و جزییات مربوط به seller
    هر محصول در ساختار جیسونی api برای همان محصول نمایش داده میشود '''
    
    class Meta:
        model = SellerProductPrice
        fields = "__all__"
      
class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    # brand_details = BrandSerializer(source='brand',read_only=True)
    ''' با استفاده از خط بالا کل اطلاعات و جزییات مربوط به brand
    هر محصول در ساختار جیسونی api برای همان محصول نمایش داده میشود '''

    category = CategorySerializer(read_only=True)
    # category_details = CategorySerializer(source='category' read_only=True)
    ''' با استفاده از خط بالا کل اطلاعات و جزییات مربوط به category
    هر محصول در ساختار جیسونی api برای همان محصول نمایش داده میشود '''

    # seller = SellerSerializer(read_only=True)
    # seller = SellerSerializer(source='sellers',many=True, read_only=True)
    # ''' با استفاده از خط بالا کل اطلاعات و جزییات مربوط به seller
    # هر محصول در ساختار جیسونی api برای همان محصول نمایش داده میشود '''

#نکته بسیار مهم: اگر نام متغیر با نام خود فیلد در کلاس اصلی یکسان باشد 
# به ست کردن و قرار دادن source نیازی نیست

    product_price_details = ProductPriceSerializer(
        source='seller_prices', many=True , read_only=True 
        ) 
    '''نکته مهم:
  چون در مدل پروداکت این فیلد SellerProductPrice با عبارت seller_prices  
   به کلاس(جدول(table)) Product در ارتباط(متصل) است یعنی
  class SellerProductPrice(models.Model):
    
  product = models.ForeignKey("Product"
                                ,verbose_name=_("Product"),
                                related_name="seller_prices"    
                                ,on_delete=models.CASCADE
                                )
  پس  در   product_price_details آرگومان source مربوط
  به سریالایزر ProductPriceSerializer را source =   "seller_price     قرار میدهیم 
    '''

    class Meta:
        model = Product
        fields = "__all__"
