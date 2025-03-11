from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
     path('register/', RegisterAPIView.as_view(), name="register-customer"),
     path('signup-verify/<str:otp>/', SignupVerifyAPIView.as_view(), name="signup_verify"),
     path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
     path('logout/',BlacklistRefreshView.as_view(), name='token_blacklist'),
     path('change-password/', ChangePasswordAPIView.as_view(), name="change-password"),
    path('request-reset-password/', RequestForForgetPassword.as_view(), name="request_forget_password"),
     path('reset-password/<str:otp>/', ForgetPassword.as_view(), name="reset_password"),
    


]