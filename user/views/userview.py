"""
View for User model
"""

from rest_framework import generics
from user.serializers.userserializer import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from user.models import User, UserRole

class CreateUserView(generics.CreateAPIView):
    """
    This view is used to create user
    """
    permission_classes = [AllowAny] # Bypass JWT for /create API
    serializer_class = UserSerializer # Uses User serializer to create user in the system