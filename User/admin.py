from django.contrib import admin
from User.models import (CustomUser, AdminUser, StaffUser,
                         MerchantUser, CustomerUser, PhoneNumber)

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(AdminUser)
admin.site.register(StaffUser)
admin.site.register(MerchantUser)
admin.site.register(CustomerUser)
admin.site.register(PhoneNumber)
