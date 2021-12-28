from django.urls import path 
from .views import RegisterAPI,VerifyOTPAPI,LoginAPI,ResentOtp
                    


urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("verify/", VerifyOTPAPI.as_view() , name="verify"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("resent_otp/", ResentOtp.as_view(), name="resent-otp")
]
