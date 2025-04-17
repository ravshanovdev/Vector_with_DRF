from django.urls import path
from .views import (
    ChatSendAPIView,
    ChatListAPIView,
    NotificationListAPIView,
    MarkNotificationAsSeenAPIView,
    UpdateOnlineStatusAPIView
)

urlpatterns = [
    path('api/send-chat/', ChatSendAPIView.as_view()),
    path('api/chat/<str:thread_name>/', ChatListAPIView.as_view()),
    path('api/notifications/', NotificationListAPIView.as_view()),
    path('api/notifications/seen/<int:pk>/', MarkNotificationAsSeenAPIView.as_view()),
    path('api/online-status/', UpdateOnlineStatusAPIView.as_view()),
]
