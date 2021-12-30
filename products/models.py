from django.db import models
from accounts.models import User
from django.utils import timezone
# Create your models here.


class Products(models.Model):
    name = models.CharField(max_length=50,unique=True)
    image = models.ImageField(upload_to='media/images/')
    description = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    discount_name = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=6, decimal_places=3)
    first_time_discount = models.DecimalField(max_digits=5, decimal_places=2 , default=100)
    def __str__(self):
        return self.name


class Customer_record(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product = models.OneToOneField(Products, on_delete=models.CASCADE)
    date_purchase = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'Customer : {self.user} , Product : {self.product}'
    
    
class Cart(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    product = models.OneToOneField(Products,on_delete=models.CASCADE)