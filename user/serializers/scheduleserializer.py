from rest_framework import serializers
from user.models import UserSchedules

class UserScheduleSerializer(serializers.ModelSerializer):
    """
     Serializer to manage user schedules
    """
    class Meta:
        model = UserSchedules
        fields = ["id","title", "start", "end", "color"]