import threading
import hashlib
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from common.response import success_response, error_response
from common.utils import send_verification_email, send_activation_success_email, GenerateKey
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterAPIView(APIView):                                                     
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data = request.data)
        
        if serializer.is_valid():
            user, otp = serializer.save()
            send_email=threading.Thread(target=send_verification_email,args=[user, otp])
            send_email.start()
            
            return success_response(message="User has been registered please verify the OTP sent to your email")
        else:
            return error_response(errors=serializer.errors, message="Problems with registration...")


class SignupVerifyAPIView(APIView):
    def post(self, request, otp):
        try:
            try:
                user = User.objects.get(otp=hashlib.sha256(otp.encode('utf-8')).hexdigest(), is_active=False)
            except Exception as e:
                return error_response(message="Invalid otp or User Not Found")

            if user.otp != hashlib.sha256(otp.encode('utf-8')).hexdigest():
                return error_response(message="Invalid Otp")
            else:
                user.is_active = True
                user.otp = None
                user.save()
                thread = threading.Thread(target=send_activation_success_email, args=(user.email,))
                thread.start()
                return success_response(message="Your account has been successfully activated!!")

        except:
            return error_response(message= "Invalid otp OR No any inactive user found for given otp")
        

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class BlacklistRefreshView(APIView):
    def post(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
        except Exception as e:
            return error_response(message=str(e))
        token.blacklist()
        return success_response(message="User access token has been blacklisted successsfully")


class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        password = request.data.get("password")
        re_password = request.data.get("re_password")
        current_password = request.data.get("current_password")

        user = request.user

        if not user.check_password(current_password):
             return error_response(error= "Incorrect current password.")
        
        try:   
            validate_password(password)   
            validate_password(re_password)
        except ValidationError as e:
            return error_response(error = "The password must contain at least 8 characters and should not be common")

     
        if password != re_password:
            return error_response(error = "Password do not match")

        user = request.user
        user.set_password(password)
        user.otp = None
        user.save()
        return success_response(message="Password updated successfully")

        
class RequestForForgetPassword(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs): 
        email=request.data.get('email')

        try:
            user_object=User.objects.get(email=email)
        except Exception as e:
             return error_response(message= "User Not Found")


        try:
            key = GenerateKey.return_value()
            hashed_otp = hashlib.sha256(key.encode('utf-8')).hexdigest()

            thread_email_send=threading.Thread(target=send_verification_email,args=[email,key])
            thread_email_send.start()
            user_object.otp=hashed_otp
            user_object.save()
            return success_response(message="otp has been sent to your email")
        except Exception as e:
            return error_response(message=str(e))
        

class ForgetPassword(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, otp):   
        
        try:
            user = User.objects.get(otp=hashlib.sha256(otp.encode('utf-8')).hexdigest(), is_active=True)
        except:
             return error_response(error ="User Not Found")


        if user.otp != hashlib.sha256(otp.encode('utf-8')).hexdigest():
            return error_response(message="Invalid otp")
        

        try:
            password = request.data.get('password')

            try:
                validate_password(password)
            except ValidationError as e:
                return error_response(error= list(e.messages)[0])
            
           
            user.set_password(password)
            user.otp = None
            user.save()
            return success_response(message="successfully updated your password")
            
        except Exception as e:
            return error_response(message=str(e)) 

