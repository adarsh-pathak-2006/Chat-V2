from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_of')
    user2=models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_with')
    created_on=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user', 'user2'], name='single_chat_constraint_per_user')]

    def __str__(self):
        return self.user.username
    
class Conversation(models.Model):
    chat=models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='convo')
    message=models.TextField()
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:100]

    
