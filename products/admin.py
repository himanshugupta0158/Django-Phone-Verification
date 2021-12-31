from django.contrib import admin
from .models import Products , Customer_record ,Cart , Category

# Register your models here.


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name' , 'price' , 'discount_name' , 'category']


@admin.register(Customer_record)
class Customer_recordAdmin(admin.ModelAdmin):
    list_display = ['user' , 'product_name' , 'date_purchase']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user' , 'product']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['product_category']