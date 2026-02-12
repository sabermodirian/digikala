from rest_framework.permissions import BasePermission , SAFE_METHODS



class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenthicated as a user, or read-only request. 
    """

    def has_permission(self , request ,view):
        """ این مجوز فقط روی لیست محصولات اجرا میشود"""
        return bool(

            request.method in SAFE_METHODS or
            request.user and request.user.is_staff
            
        )