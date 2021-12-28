from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=14 , unique=True)
    is_number_verified = models.BooleanField(default=False)
    username = models.CharField( max_length=50)
    email = models.EmailField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'phone_number'
    
    REQUIRED_FIELDS = ['username' , 'email']
    
    def __str__(self):
        return self.username
    
    