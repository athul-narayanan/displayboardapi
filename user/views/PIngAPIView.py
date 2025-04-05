"""
View for User model
"""

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import AllowAny


class PingAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny] # Bypass JWT for /create API
    """
        This view is used to update ping from node mcu
    """
    @extend_schema(
    parameters=[
        OpenApiParameter(
            name='email',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='',
            required=False
        ),
    ])
    
    def post(self, request):
        try:
            email = request.query_params.get('email')
            if id is None:
                return Response({
                    'error': 'Invalid request',
                }, status=status.HTTP_400_BAD_REQUEST)
        
            user = User.objects.get(email=email)
            user.ping_started = True
            user.save()
            return Response({
                'message': "Ping Successful"
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
             return Response({
                    'error': 'User does not exist',
             }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                'message': "Invalid request"
            }, status=status.HTTP_400_BAD_REQUEST)

    