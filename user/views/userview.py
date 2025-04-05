"""
View for User model
"""

from rest_framework import generics
from user.serializers.userserializer import UserSerializer
from rest_framework.permissions import AllowAny

class CreateUserView(generics.CreateAPIView):
    """
    This view is used to create user
    """
    permission_classes = [AllowAny] # Bypass JWT for /create API
    serializer_class = UserSerializer # Uses User serializer to create user in the system