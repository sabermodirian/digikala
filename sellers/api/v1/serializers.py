# from products.api.v1.models import User
from ...models import Seller # noqa: F401 #== معادل خط بالا

from rest_framework import serializers
 
# from django.contrib.auth.models import User  
from django.contrib.auth import get_user_model



User = get_user_model() # این خط خودش میفهمه یوزر الان کیه (accounts.User)



class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Seller
        fields = "__all__"

      



    
