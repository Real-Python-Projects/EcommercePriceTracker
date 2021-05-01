from django.contrib import admin
from User.models import (CustomUser, AdminUser, StaffUser,
                         MerchantUser, CustomerUser, PhoneNumber, Profile,
                         EmailSubscibers)
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'is_superuser',
                'is_staff',
                'is_merchant',
                'is_customer',
            ),
        }),
    )
    
    
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(AdminUser)
admin.site.register(StaffUser)
admin.site.register(MerchantUser)
admin.site.register(CustomerUser)
admin.site.register(PhoneNumber)
admin.site.register(Profile)
admin.site.register(EmailSubscibers)