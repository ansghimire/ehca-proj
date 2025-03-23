#import
import hashlib
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserAccount
from common.utils import GenerateKey

#class
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserAccount
        fields = ('email', 'first_name', 'last_name', 'password', 'otp')
    
    def create(self, validated_data):

        request = self.context.get('request')
       
        key = GenerateKey.return_value()
        hashed_otp = hashlib.sha256(key.encode('utf-8')).hexdigest()
        # Validate and set password
        password = validated_data.pop('password')

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"success":False,'error': list(e.messages)[0]})

        # Create CustomUser instance
        user = UserAccount.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            otp=hashed_otp,
            is_client =   True if request.data.get('is_client') else False,
            is_staff =   True if request.data.get('is_nurse') else False,
            password = password
        )
        user.is_active = False
        user.save()

        return user.email, key

    
    def set_password(self, user, password):
        # Validate password
        try:
            validate_password(password, user)
        except ValidationError as e:
            # Raise validation error with proper formatting
            raise serializers.ValidationError({'password': list(e.messages)})

        # Set password
        user.set_password(password)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
      
        access_token = data['access']
        refresh_token = data['refresh']

        response_data = {
            "success": True,
            "message": "User logged in successfully",
            "data": {
                "access": access_token,
                "refresh": refresh_token,
                "full_name" : f'{self.user.first_name} {self.user.last_name}',
      
            }
        }

        return response_data
    


