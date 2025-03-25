"""
View for User model
"""

from rest_framework import generics
from user.serializers.scheduleserializer import UserScheduleSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from user.models import User, UserSchedules
from datetime import datetime


class UserScheduleView(generics.CreateAPIView):
    """
    This view is used to manage user schedules
    """

    serializer_class = UserScheduleSerializer # Uses userschedules serializer to manage user schedules

    def get(self, request):
        id = request.data.get("id")
        month = request.data.get("month") 
        if month is None:
            month = datetime.now().month
        if month < 0 or month > 12:
            return Response({
                'error': 'Invalid month',
            }, status=status.HTTP_400_BAD_REQUEST)
        schedules = UserSchedules.objects.filter(start__month=month,id=id )
        serializedData = self.serializer_class(schedules,many=True)
        return Response(serializedData.data,status=status.HTTP_201_CREATED)
    
    def post(self, request):
        serializedData = UserScheduleSerializer(data=request.data)
        if serializedData.is_valid():
            schedule = UserSchedules.objects.create(user=request.user,**serializedData.validated_data)
            return Response({
                'message': 'Schedule created successfully',
                'id': schedule.id
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Failed to create schedule',
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        try:
            id = request.data.get("id")
            if id is None:
                return Response({
                    'error': 'Invalid request',
                }, status=status.HTTP_400_BAD_REQUEST)
        
            UserSchedules.objects.get(id=id).delete()
            
            return Response({
                    'message': 'Schedule deleted successfully',
            }, status=status.HTTP_200_OK)
        except UserSchedules.DoesNotExist:
             return Response({
                    'error': 'Schedule does not exist',
             }, status=status.HTTP_400_BAD_REQUEST)