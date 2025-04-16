# # chat/serializers.py
#
# from rest_framework import serializers
# from .models import Room, Message
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username')
#
#
# class ChatRoomSerializer(serializers.ModelSerializer):
#     members = UserSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Room
#         fields = ('id', 'name', 'members', 'created_at')
#
#
# class CreateRoomSerializer(serializers.ModelSerializer):
#     user_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
#
#     class Meta:
#         model = Room
#         fields = ('id', 'name', 'user_ids')
#
#     def create(self, validated_data):
#         user_ids = validated_data.pop('user_ids')
#         room = Room.objects.create()
#         room.members.set(user_ids)
#         return room
#
#
# class MessageSerializer(serializers.ModelSerializer):
#     sender = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Message
#         fields = ('id', 'room', 'sender', 'content', 'timestamp')
