# # chat/views.py
#
# from rest_framework import generics, permissions
# from .models import Room, Message
# from .serializers import ChatRoomSerializer, CreateRoomSerializer, MessageSerializer
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
#
# class CreateChatRoomView(generics.CreateAPIView):
#     serializer_class = CreateRoomSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
# class ListChatRoomsView(generics.ListAPIView):
#     serializer_class = ChatRoomSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         return Room.objects.filter(members=self.request.user)
#
#
# class ListMessagesView(generics.ListAPIView):
#     serializer_class = MessageSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         room_id = self.kwargs['room_id']
#         return Message.objects.filter(room_id=room_id).order_by('timestamp')
#
#
# class SendMessageView(generics.CreateAPIView):
#     serializer_class = MessageSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(sender=self.request.user)
