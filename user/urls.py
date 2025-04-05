"""
defines url mapping for the user API
"""

from django.urls import path
from user.views.authenticationview import AuthenticationView
from user.views.userscheduleview import UserScheduleView
from user.views.userview import CreateUserView
from user.views.PIngAPIView import PingAPIView

urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('login/', AuthenticationView.as_view()),
    path('schedule', UserScheduleView.as_view()),
    path('ping', PingAPIView.as_view())
]