from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import pickle
from rest_framework.exceptions import AuthenticationFailed


   
class AuthenticationSerializer(serializers.Serializer):
    """
    Serializer for Authentication.
    """

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    

    def validate(cls, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
           raise AuthenticationFailed("User name or password is wrong")
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return {
            'refresh': str(refresh),    
            'access': str(access_token),
            'email': user.email,
            'firstname': user.firstname,
            'lastname' : user.lastname,
            'usertype': user.role.role_name
        }