from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ChatModel, ChatNotification, UserProfileModel
from .serializers import ChatSerializer, ChatNotificationSerializer, UserProfileSerializer


class ChatSendAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "sent", "data": serializer.data}, status=201)
        return Response(serializer.errors, status=400)


class ChatListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, thread_name):
        chats = ChatModel.objects.filter(thread_name=thread_name).order_by('timestamp')
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)


class NotificationListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = ChatNotification.objects.filter(user=request.user, is_seen=False)
        serializer = ChatNotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class MarkNotificationAsSeenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notif = ChatNotification.objects.get(pk=pk, user=request.user)
            notif.is_seen = True
            notif.save()
            return Response({"status": "seen"})
        except ChatNotification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=404)


class UpdateOnlineStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            profile = UserProfileModel.objects.get(user=request.user)
            profile.online_status = request.data.get('online_status', False)
            profile.save()
            return Response({"status": "updated", "online": profile.online_status})
        except UserProfileModel.DoesNotExist:
            return Response({"error": "UserProfile not found"}, status=404)
