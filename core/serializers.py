from rest_framework.serializers import ModelSerializer
from core.models import Chat, Conversation
from django.contrib.auth.models import User

class RegisterSerailizer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'password']

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email']

class ConversationSerializer(ModelSerializer):
    class Meta:
        model=Conversation
        fields=['message', 'time']

class ChatSerializer(ModelSerializer):
    convo=ConversationSerializer(read_only=True)
    class Meta:
        model=Chat
        fields=['user', 'user2', 'convo']