from .serializers import UserRegisterSerializer,UserInfoSerializer,UserChangePasswordSerializer

from ...models import User  # noqa: F401
# from accounts.api.v1.models import User معادل خط بالا

from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(["POST"]) #چون قرار ه که فقط ورود اطلاعات و ثبت نام کاربر برای اولین بار باشه فقط متد POST میپذیرد
def user_register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


@api_view(["POST","GET"])
@permission_classes(IsAuthenticated)
def user_info(request):
    user = request.user
    if request.method =="GET":
        serializer = UserInfoSerializer(instance=user ,data=request.data)
        return Response(serializer.data)
    else:
        serializer = UserInfoSerializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(["POST",])
@permission_classes(IsAuthenticated)
def user_change_password(request):
    user = request.user
    serializer = UserChangePasswordSerializer(instance=user, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)