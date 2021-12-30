from django.db import models
from django.db.models import fields
from .models import Products , Customer_record
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id','name' , 'image' , 'description' , 'price' , 'discount_name' , 'discount']
        

class CustomerRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_record
        fields = ['user' , 'product_name' , 'date_purchase']
