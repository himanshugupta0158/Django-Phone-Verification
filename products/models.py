from django.db import models
from accounts.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Category(models.Model):
    product_category = models.CharField(_("Category"), max_length=50)
    
    def __str__(self):
        return self.product_category
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Products(models.Model):
    name = models.CharField(max_length=50,unique=True)
    image = models.ImageField(upload_to='media/images/')
    description = models.CharField(max_length=150)
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    discount_name = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=6, decimal_places=3)
    first_time_discount = models.DecimalField(max_digits=5, decimal_places=2 , default=100)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


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



