"""

"""

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import AllowAny
import requests


class QuickUpdateView(generics.CreateAPIView):
    """
        This view is perform quick update of schedule
    """
    @extend_schema(
    parameters=[
        OpenApiParameter(
            name='message',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='',
            required=True
        ),
    ])
    
    def post(self, request):
        try:
            message = request.query_params.get('message')
            if message is None:
                return Response({
                    'error': 'Invalid request',
                }, status=status.HTTP_400_BAD_REQUEST)
        
            user = User.objects.get(email=request.user.email)
            user.ping_started = False
            user.save()
            message = message.replace(" ", "+")
            message = message.ljust(16, "+")
            name = user.firstname + "+" + user.lastname
            name = name.ljust(16,"+")
            
            # Call node MCU API and update the message
            url = f'http://10.8.4.100/updateMessage?message={message}&name={name}'
            print(url)
            headers = {
                'Content-Type': 'application/json',
            }

            requests.get(url, headers=headers)

            return Response({
                'message': "Quick update successful"
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
             return Response({
                    'error': 'User does not exist',
             }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                'message': "Invalid request"
            }, status=status.HTTP_400_BAD_REQUEST)

    