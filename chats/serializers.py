from rest_framework import serializers
from .models import UserProfileModel, ChatModel, ChatNotification
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfileModel
        fields = ['user', 'name', 'online_status']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = ['id', 'sender', 'message', 'thread_name', 'timestamp']


class ChatNotificationSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ChatNotification
        fields = ['id', 'chat', 'user', 'is_seen']
