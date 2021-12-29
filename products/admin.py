from django.contrib import admin
from .models import Products , Customer_record

# Register your models here.


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name' , 'price' , 'discount_name']


@admin.register(Customer_record)
class Customer_recordAdmin(admin.ModelAdmin):
    list_display = ['user' , 'product_name' , 'date_purchase']
