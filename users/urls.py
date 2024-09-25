from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUserApiView.as_view()),
    path('register/phonenumber/', PhonenumberOTPRegisterApiView.as_view()),
    
    path('otp/confirm/', ConfirmOtpAPiView.as_view()),
    path('otp/resend/', ResendOtpApiView.as_view()),
    path('otp/set/password/', SetUserPasswordApiView.as_view()),
    path('otp/phone/resend/', PhonenumberSendOTPApiView.as_view()),
    
    path('user/', UserApiView.as_view()),
    path('user/password/change/', ChangeUserPasswordApiView.as_view()),

    path('user/profile/', ProfileApiView.as_view()),
    path('user/profile/modify/<int:id>/', ProfileModifyApiView.as_view()),

    path('email/check/', EmailCheckApiView.as_view()),

]