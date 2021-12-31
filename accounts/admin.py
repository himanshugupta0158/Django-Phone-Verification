from django.contrib import admin
from .models import User , UserOTP

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User 
    list_filter = ('phone_number' , 'username' ,'firstname' , 'lastname','is_active' , 'is_staff')
    list_display = ('phone_number' , 'username')
    
    fieldsets = (
        ('User Info',{"fields" : ('phone_number', 'username' ,'firstname' , 'lastname' ,'email',)}),
        ('Permissions' ,{'fields' : ('is_staff' , 'is_active' , 'is_superuser' ,'is_first_time')})
    )
    
@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number' , 'otp')
    