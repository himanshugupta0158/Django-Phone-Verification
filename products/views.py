from django.shortcuts import render
from rest_framework.serializers import Serializer
from .models import Products , Customer_record

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializer , CustomerRecordSerializer
# Create your views here.


class ProductAPIView(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    lookup_field = 'id'
    
    def get_object(self , id):
        try:
            return Products.objects.filter(id=id).first()
        except Products.DoesNotExist :
            return None
    
    def get(self , request , id = None):
        if id is None :
            product = self.get_queryset()
            serializer = self.get_serializer(product , many=True)
            return Response(serializer.data)
        else:
            query = self.get_object(id)
            if query :
                serializer = self.get_serializer(query)
                return Response(serializer.data)
            else:
                return Response({} , status = status.HTTP_404_NOT_FOUND)




class CustomerRecordAPIView(GenericAPIView):
    serializer_class = CustomerRecordSerializer
    queryset = Customer_record.objects.all()
    lookup_field = 'id'
    
    def get_object(self , id):
        try:
            return Customer_record.objects.get(id)
        except Customer_record.DoesNotExist :
            return None
    
    def get(self , request , id = None):
        if id is None :
            product = self.get_queryset()
            serializer = self.get_serializer(product , many=True)
            return Response(serializer.data)
        else:
            query = self.get_object(id)
            if query :
                serializer = self.get_serializer(query)
                return Response(serializer.data)
            else:
                return Response({} , status = status.HTTP_404_NOT_FOUND)

