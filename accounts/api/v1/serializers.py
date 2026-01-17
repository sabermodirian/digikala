from accounts.api.v1.models import User
# from ...models import User #== معادل خط بالا

from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    '''این سریالایزر مخصوص ثبت نام و ایجاد و ساخت کاربر در سایت میباشد '''
    
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','mobile','password']
        read_only_fields = ('id',) # در زمان create کردن سریالایزر به id نیازی نیست 
        write_only_fields = ('password',) # را برگردونه و نشون بده password در زمان فرستادن ریسپانس توسط سریالایزر نمیخام که این  

    def update(self,instance, validated_data):
        ''' برای اینکه بهیچ وجه نشود که متد آپدیت را برای این سریالایزر صدا کرد'''
        raise Exception('Don,t Call Updating On This Serializer:UserRegisterSerializer')

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
        read_only_fields = ('date_joined','last_login') # در زمان آپدیت نیازی به آپدیت کردن این دوتا نیست
        # write_only_fields = 

class UserChangePasswordSerializer(serializers.ModelSerializer):
    ''' این سریالایزر جهت تغییر کلمه عبور در سایت برای هرکاربر مجاز تعبیه میشود'''

    class Meta:
        model = User
        fields = ['password','new_password']
        write_only_fields = ['password','new_password']
    
    def update(self, instance, validated_data):
        if instance.check_password(validated_data['password']):
            instance.set_password(validated_data['new_password'])
            instance.save()
        else:
            raise serializers.ValidationError(
                {"password_detail":"پسورد جدید و قدیمت باهم یکی نیستن"}
            )
        return instance

# برای مثال کاربر شماره id=5 میخایم کلمه یعورش رو آپدیت کنیم
# serializer=UserChangePasswordSerializer(
#     instance=User.Objects.get(id=5),
#     data=request.data
#     )
