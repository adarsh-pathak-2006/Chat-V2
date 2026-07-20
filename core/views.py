from django.shortcuts import get_object_or_404
from core.models import Chat, Conversation
from django.contrib.auth.models import User
from core.serializers import ChatSerializer, ConversationGetSerializer, ConversationPostSerializer, RegisterSerailizer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chat.throttles import RegisterationThrottle, TokenObtainThrottle, GeneralThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q


class RegisterAPI(APIView):
    throttle_classes=[RegisterationThrottle]
    def post(self, request):
        serial=RegisterSerailizer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            email=serial.validated_data['email']
            password=serial.validated_data['password']

            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return Response({'user_err':'user already exists'}, status=403)
            else:
                User.objects.create_user(username=username, email=email, password=password)
                return Response({'success':'user created successfully'}, status=201)    
        else:
            return Response(serial.errors, status=400)
        
class CustomTokenObtainView(TokenObtainPairView):
    throttle_classes=[TokenObtainThrottle]


class ChatAPI(APIView):
    permission_classes=[IsAuthenticated]
    throttle_classes=[GeneralThrottle]
    def get(self, request):
        data=Chat.objects.filter(Q(user=request.user) | Q(user2=request.user))
        serial=ChatSerializer(data, many=True)
        return Response(serial.data, status=200)
    
    def post(self, request):
        serial=ChatSerializer(data=request.data)
        if serial.is_valid():
            serial.save(user=request.user)
            return Response(serial.data, status=201)
        else:
            return Response(serial.errors, status=400)
        
class ConversationAPI(APIView):
    def get(self, request, pk):
        chat_data=get_object_or_404(Chat, Q(user=request.user) | Q(user2=request.user), id=pk)
        data=Conversation.objects.filter(chat=chat_data)
        serial=ConversationGetSerializer(data, many=True)
        return Response(serial.data, status=200)
    
    def post(self, request, pk):
        serial=ConversationPostSerializer(data=request.data)
        if serial.is_valid():
            chat_data=get_object_or_404(Chat, Q(user=request.user) | Q(user2=request.user), id=pk)
            serial.save(chat=chat_data, user=request.user)
            return Response(serial.data, status=201)
        else:
            return Response(serial.errors, status=400)



            

