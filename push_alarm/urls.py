from django.urls import path, include
from .views import *

urlpatterns = [
    path('device-token', DeviceTokenView.as_view()),
    path('comment', CommentPushAlarmView.as_view()),
    path('notification-list', GetAllNotificationView.as_view())
]