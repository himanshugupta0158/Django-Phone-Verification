import random
import os
from django.shortcuts import render , redirect
from django.contrib.auth import login , logout
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .serializers import RegisterSerializer , LoginSerializer , OTPVerificationSerializer

from .models import User
from twilio.rest import Client
# Create your views here.

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

otp = None

def send_otp(request,new_otp):
    otp = new_otp
    request.session['otp'] = otp
    message = client.messages.create(
        body=f"Here is the OTP {otp} for account activation.",
        from_='+12344053612',
        to='+91'+str(request.data['phone_number'])
    )


class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer
    
    
    @csrf_exempt
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            request.session['phone_number'] = request.data['phone_number']
            send_otp(request,random.randint(10000,99999))
            user = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors , status = 400)

class VerifyOTPAPI(GenericAPIView):
    serializer_class = OTPVerificationSerializer
    
    @csrf_exempt
    def post(self , request):
        print("OTP : ",request.session['otp'])
        print("OTP : ",request.data['otp'])
        if int(request.data['otp']) == int(request.session['otp']) :
            user = User.objects.filter(phone_number=request.session['phone_number']).first()
            user.is_active = True 
            user.save()
            print("OTP : ",request.session['otp'])
            del request.session['otp']
            del request.session['phone_number']
            return Response({'result' : 'OTP verified successfully'} , status=200)
        
        return Response({'result' : 'Invalid OTP'} , status=400)

class ResentOtp(GenericAPIView):
    serializer_class = LoginSerializer
    
    @csrf_exempt
    def post(self, request):
        phone_number = request.data['phone_number']
        user = User.objects.filter(phone_number=phone_number).first()
        if user :
            send_otp(request,random.randint(10000,99999))
            return Response({'result' : 'OTP sent successfully'} , status=400)
            
        else:
            del request.session['phone_number']
            return redirect('register')
    
    


class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer
    
    @csrf_exempt
    def post(self, request):
        request.session['phone_number'] = request.data['phone_number']
        user = User.objects.filter(phone_number=request.session['phone_number']).first()
        if user :
            if user.is_active == True :
                login(request , user)
                return Response({"Result" : "User Logged in Successfully"} , status = 201)
            else:
                return Response({"Result" : "User's account is not active check your mobile number's SMS."} , status = 400)
        else:
            del request.session['phone_number']
            return redirect('register')
        
        
