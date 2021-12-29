from django.urls import path 
from .views import RegisterAPI,VerifyOTPAPI,LoginAPI,LogoutAPI,HomeAPI
                    


urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("verify_otp/", VerifyOTPAPI.as_view() , name="verify-otp"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("logout/", LogoutAPI.as_view(), name="logout"),
    path("home/", HomeAPI.as_view(), name="home"),
    
]
