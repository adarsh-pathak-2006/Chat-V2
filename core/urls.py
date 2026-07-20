from django.urls import path
from core.views import ChatAPI, ConversationAPI

urlpatterns = [
    path('chat/', ChatAPI.as_view(), name='chat'),
    path('conversation/', ConversationAPI.as_view(), name='conversation'),
]
