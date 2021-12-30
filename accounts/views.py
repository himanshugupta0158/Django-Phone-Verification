import random
import os
from django.contrib.auth.models import Permission
from django.shortcuts import render , redirect
from django.contrib.auth import login , logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from .serializers import RegisterSerializer , LoginSerializer , OTPVerificationSerializer

from .models import User

# twilio helps to sent SMS to mobile number but it need to be register on twilio site.
from twilio.rest import Client

# Create your views here.

# setting accounts_id and auth_token for SMS
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

otp = None

# os.environ['TWILIO_TRIAL_PHONE_NUMBER']

# body code for message sending
def send_otp(request,new_otp):
    otp = new_otp
    # saving new otp in session
    request.session['otp'] = otp
    message = client.messages.create(
        body=f"Here is the OTP {otp} for account activation.",
        from_=os.environ['TWILIO_TRIAL_PHONE_NUMBER'],
        to='+91'+str(request.data['phone_number'])
    )


# registering new user
class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer
        
    def get(self , request):
        return Response({'Message' : 'Register Yourself'})
    
    @csrf_exempt
    def post(self, request):
        if request.session['otp'] :
            serializer = self.get_serializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                del request.session['otp']
                return redirect('login')
            return Response(serializer.errors , status = 400)
        else:
            return redirect('login')

# verifying user both for login and register 
class VerifyOTPAPI(GenericAPIView):
    serializer_class = OTPVerificationSerializer
    
    def get(self , request):
        return Response({'Message' : 'Verify Your OTP'})
        
    @csrf_exempt
    def post(self , request):
        print("OTP : ",request.session['otp'])
        print("OTP : ",request.data['otp'])
        if request.session['otp'] :
            if int(request.data['otp']) == int(request.session['otp']) :
                user = User.objects.filter(phone_number=request.session['phone_number']).first()
                if user :
                    user.is_active = True 
                    user.save()
                    login(request , user)
                    print('logging in')
                    request.session['login_user'] = user.username
                    return redirect('home')
                else:
                    return redirect('register')
        else:
            return Response({'result' : 'Regenerate OTP for login'} , status=401)   
        return Response({'result' : 'Invalid OTP'} , status=400)
    

# logging and registering both user have to verify phone number
class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer
    
    
    def get(self , request):
        return Response({'Message' : 'For User Login and Register , Enter you Phone Number and verify it.'})
    
    @csrf_exempt
    def post(self, request):
        request.session['phone_number'] = request.data['phone_number']
        send_otp(request,random.randint(10000,99999))
        return redirect('verify-otp')
    

# logging out users
class LogoutAPI(GenericAPIView):

    def get(self,request):
        try:
            logout(request)
            del request.session['otp']
            del request.session['phone_number']
            return Response({'result' : 'User loggout successfully'} , status=200)        
        except:
            return redirect('login')
            



# Home page content will be seen by user if they are logged in.
class HomeAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self , request):
        return Response({'Home' : 'This is Home Page'} , status=201)
    
