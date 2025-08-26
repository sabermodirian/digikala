from django.contrib import admin
from accounts.models import User
from django.utils.translation import gettext_lazy as _ # مطمئن شوید این ایمپورت را دارید
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.



class UserAdmin(BaseUserAdmin):
    list_display = ['email' ,'mobile' ,'first_name' , 'last_name' , 'is_active']
    ordering = ['email']
    search_fields = ['date_joined','last_login']
    add_fieldsets = [
        (None , {
            'classes': ('wide',),
            'fields' : ('email' ,'mobile', 'password1' , 'password2')
        }),
    ]

    fieldsets = ( # شروع تاپل اصلی fieldsets
        (None, { # اولین تاپل
            "fields": (
                'mobile',
                'email',
                'password'
            ),
        }),
        (_('Personal info'),{ # دومین تاپل
            "fields":('first_name' , 'last_name' )
        }),
        (_('Permissions'),{ # سومین تاپل
            "fields":('is_staff' , 'is_active','is_superuser')
        }),
        (_('Important dates'),{ # چهارمین تاپل
            "fields":('last_login' ,'date_joined')
        }),
    ) # پایان تاپل اصلی fieldsets

admin.site.register(User,UserAdmin)

