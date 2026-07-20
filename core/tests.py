from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.models import Chat, Conversation

User = get_user_model()

class RegistrationTests(APITestCase):
    def test_registration_success(self):
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_duplicate_username(self):
        User.objects.create_user(username='testuser', email='original@example.com', password='password')
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'new@example.com', 'password': 'password123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_registration_duplicate_email(self):
        User.objects.create_user(username='originaluser', email='test@example.com', password='password')
        url = reverse('register')
        data = {'username': 'newuser', 'email': 'test@example.com', 'password': 'password123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

class ChatAndConversationTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password')
        self.user3 = User.objects.create_user(username='user3', email='user3@example.com', password='password')
        
        # User 1 logs in
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'username': 'user1', 'password': 'password'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_chat(self):
        url = reverse('chat')
        data = {'user2': self.user2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(Chat.objects.first().user, self.user1)

    def test_list_chats_visibility(self):
        chat = Chat.objects.create(user=self.user1, user2=self.user2)
        
        # user1 fetches chats
        url = reverse('chat')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        
        # user2 logs in and fetches chats
        token_url = reverse('token_obtain_pair')
        res2 = self.client.post(token_url, {'username': 'user2', 'password': 'password'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res2.data['access'])
        
        response2 = self.client.get(url)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(response2.data[0]['id'], chat.id)

        # user3 logs in and should see NO chats
        res3 = self.client.post(token_url, {'username': 'user3', 'password': 'password'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res3.data['access'])
        
        response3 = self.client.get(url)
        self.assertEqual(len(response3.data), 0)

    def test_create_and_fetch_conversations(self):
        chat = Chat.objects.create(user=self.user1, user2=self.user2)
        url = reverse('conversation', kwargs={'pk': chat.id})
        
        # User 1 sends message
        self.client.post(url, {'message': 'Hello from user1'})
        
        # User 2 logs in and sends message
        token_url = reverse('token_obtain_pair')
        res2 = self.client.post(token_url, {'username': 'user2', 'password': 'password'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res2.data['access'])
        
        self.client.post(url, {'message': 'Hello back from user2'})
        
        # User 2 fetches messages
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['message'], 'Hello from user1')
        self.assertEqual(response.data[1]['message'], 'Hello back from user2')
