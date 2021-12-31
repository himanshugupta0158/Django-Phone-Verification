from django.db import models
from django.db.models import fields
from .models import Products , Customer_record
from rest_framework import serializers
from .models import Products , Category ,Cart , Customer_record


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id','name' , 'image' , 'description' , 'category' , 'price' , 'discount_name' , 'discount']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['product_category']

class CustomerRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_record
        fields = ['user' , 'product_name' , 'date_purchase']
