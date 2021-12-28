from rest_framework import serializers
from django.utils.translation import gettext_lazy
from .models import User 



class RegisterSerializer(serializers.ModelSerializer):
    class Meta :
        model = User 
        fields = ['phone_number' , 'username' , 'email']
        
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['phone_number']

class OTPVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField()
    class Meta :
        model = User
        fields=['otp']