# from ...models import User #== 
from accounts.api.v1.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    '''این سریالایزر مخصوص ثبت نام و ایجاد و ساخت کاربر در سایت میباشد '''
    
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','mobile','password']
        read_only_fields = ('id',) # در زمان create کردن سریالایزر به id نیازی نیست 

    def create(self, validated_data):
        user = super().create(validated_data)
        #TODO : some actions مثل --> پیامک زدن یا ایمیل زدن یا خوشامدگویی پیغام 
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    ''' این سریالایزر برای نمایش اطلاعات کاربر رجیستر و احراز هویت شده  در سایت میباشد'''

    class Meta:
        model = User
        fields = [
            'first_name','last_name','email','mobile','password','date_joined'
            ,'last_login'] #TODO: last_login puts in django>contribe>auth>base_user.py> class AbstractBaseUser(models.Model):


class UserChangePasswordSerializer(serializers.ModelSerializer):
    ''' این سریالایزر جهت تغییر کلمه عبور در سایت برای هرکاربر مجاز تعبیه میشود'''

    class Meta:
        model = User
        fields = ['password','new_password']