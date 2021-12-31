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

from .models import User , UserOTP

# twilio helps to sent SMS to mobile number but it need to be register on twilio site.
from twilio.rest import Client

# Create your views here.

# setting accounts_id and auth_token for SMS
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# os.environ['TWILIO_TRIAL_PHONE_NUMBER']

# body code for message sending
def send_otp(otp):
    message = client.messages.create(
        body=f"Here is the OTP {otp.otp} for phone number verification.",
        from_=os.environ['TWILIO_TRIAL_PHONE_NUMBER'],
        to='+91'+str(otp.phone_number)
    )


# registering new user
class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer
        
    def get(self , request):
        return Response({'Message' : 'Register Yourself'})
    
    @csrf_exempt
    def post(self, request):
        otp = UserOTP.objects.filter(phone_number=request.data['phone_number'])
        if otp :
            serializer = self.get_serializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return redirect('login')
            return Response(serializer.errors , status = 400)
        else:
            request.session['login_msg'] = 'OTP not found for this number.Login in again'
            return redirect('login')

# verifying user both for login and register 
class VerifyOTPAPI(GenericAPIView):
    serializer_class = OTPVerificationSerializer
    
    def get(self , request):
        return Response({'Message' : 'Verify Your OTP'})
        
    @csrf_exempt
    def post(self , request):
        otp = UserOTP.objects.filter(phone_number=request.session['phone_number']).first()
        if otp :
            if int(request.data['otp']) == int(otp.otp) :
                user = User.objects.filter(phone_number=otp.phone_number).first()
                if user :
                    if user.is_active == False :
                        user.is_active = True 
                        user.save()
                    else:
                        pass
                    login(request , user)
                    print('logging in')
                    UserOTP.objects.filter(phone_number=otp.phone_number).delete()
                    return redirect('home')
                else:
                    return redirect('register')
            else:
                request.session['login_msg'] = 'Invalid OTP'
                return redirect('login')
        else:
            request.session['login_msg'] = 'Regenerate OTP for login or register , OTP not found.'
            return redirect('login')
    

# logging and registering both user have to verify phone number
class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer
    
    
    def get(self , request):
        try:
            print('try')
            if request.session['login_msg'] :
               return Response({'Message' :request.session['login_msg'] }) 
            else:
               return Response({'Message' : 'For User Login and Register , Enter you Phone Number and verify it.'})
        except:
            print('except')
            return Response({'Message' : 'For User Login and Register , Enter you Phone Number and verify it.'})
    
    @csrf_exempt
    def post(self, request):
        try:
            del request.session['login_msg']
        except:
            pass
        request.session['phone_number'] = request.data['phone_number']
        UserOTP.objects.filter(phone_number=request.data['phone_number']).delete()
        otp_details = UserOTP(phone_number=request.data['phone_number'] , otp = random.randint(10000,99999))
        otp_details.save()
        send_otp(otp_details)
        return redirect('verify-otp')
    

# logging out users
class LogoutAPI(GenericAPIView):

    def get(self,request):
        try:
            logout(request)
            return Response({'result' : 'User loggout successfully'} , status=200)        
        except:
            return redirect('login')
            



# Home page content will be seen by user if they are logged in.
class HomeAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self , request):
        user = request.user
        UserOTP.objects.filter(phone_number=user.phone_number).delete()
        return Response({'Home' : 'This is Home Page'} , status=201)
    
