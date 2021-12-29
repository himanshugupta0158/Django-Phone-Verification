from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
# Create your models here.

# New User model(table for database)
class User(AbstractUser):
    phone_number = models.CharField(max_length=14 , unique=True)
    username = models.CharField( max_length=50)
    email = models.EmailField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_first_time = models.BooleanField(default=False) 
    
    # objects used for allowing all fields of this db be used and change old user table.
    objects = CustomUserManager()
    
    # username field require for making user logged in.
    USERNAME_FIELD = 'phone_number'
    
    # require fields for important fields data should be filled in.
    REQUIRED_FIELDS = ['username' , 'email']
    
    def __str__(self):
        return self.username
    
