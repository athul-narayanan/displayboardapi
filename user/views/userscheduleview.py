"""
View for User model
"""

from rest_framework import generics
from user.serializers.scheduleserializer import UserScheduleSerializer
from rest_framework.response import Response
from rest_framework import status
from user.models import User, UserSchedules
from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter


class UserScheduleView(generics.CreateAPIView):
    """
    This view is used to manage user schedules
    """

    serializer_class = UserScheduleSerializer # Uses userschedules serializer to manage user schedules

    @extend_schema(
    parameters=[
        OpenApiParameter(
            name='month',
            type=int,
            location=OpenApiParameter.QUERY,
            description='Month (1-12). If not provided, current month is used.',
            required=False
        ),
    ],
    responses={200: UserScheduleSerializer(many=True)},
    )
    def get(self, request):
        default_month = datetime.now().month
        try:
            month = int(request.query_params.get('month', default_month))
            if month is None:
                month = datetime.now().month
            if month < 0 or month > 12:
                return Response({
                    'error': 'Invalid month',
                }, status=status.HTTP_400_BAD_REQUEST)
            schedules = UserSchedules.objects.filter(start__month=month,user=request.user )
            serializedData = self.serializer_class(schedules,many=True)
            return Response(serializedData.data,status=status.HTTP_200_OK)
        except Exception:
            return Response({
                'error': 'Failed to fetch user schedules',
            }, status=status.HTTP_400_BAD_REQUEST)


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

    @extend_schema(
    parameters=[
        OpenApiParameter(
            name='id',
            type=int,
            location=OpenApiParameter.QUERY,
            required=False
        ),
    ],
    responses={200},
    )  
    def delete(self, request):
        try:
            id = int(request.query_params.get('id'))
            if id is None:
                return Response({
                    'error': 'Invalid request',
                }, status=status.HTTP_400_BAD_REQUEST)
        
            UserSchedules.objects.get(id=id, user=request.user).delete()
            
            return Response({
                    'message': 'Schedule deleted successfully',
            }, status=status.HTTP_200_OK)
        except UserSchedules.DoesNotExist:
             return Response({
                    'error': 'Schedule does not exist for the user',
             }, status=status.HTTP_400_BAD_REQUEST)