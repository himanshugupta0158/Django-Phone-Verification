from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User 
    list_filter = ('phone_number' ,'username','is_active' , 'is_staff')
    list_display = ('phone_number' ,'username')
    
    fieldsets = (
        ('User Info',{"fields" : ('phone_number', 'username' ,'email',)}),
        ('Permissions' ,{'fields' : ('is_staff' , 'is_active' , 'is_superuser' ,'is_first_time')})
    )
    
    