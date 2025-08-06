from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .serializers import UserSerializer

class UserSerializerTest(TestCase):
    """Test cases for UserSerializer."""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_create_user(self):
        """Test user creation through serializer."""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_validate_email_uniqueness(self):
        """Test email uniqueness validation."""
        User.objects.create_user(
            username='existinguser',
            email='test@example.com',
            password='pass123'
        )
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
    
    def test_validate_username_uniqueness(self):
        """Test username uniqueness validation."""
        User.objects.create_user(
            username='testuser',
            email='existing@example.com',
            password='pass123'
        )
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
    
    def test_validate_password_strength(self):
        """Test password strength validation."""
        weak_password_data = self.user_data.copy()
        weak_password_data['password'] = '123'
        serializer = UserSerializer(data=weak_password_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
    
    def test_validate_required_fields(self):
        """Test required fields validation."""
        incomplete_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        serializer = UserSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

class UserAPITest(APITestCase):
    """Test cases for User API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_register_user_success(self):
        """Test successful user registration."""
        response = self.client.post('/api/users/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['message'], 'User created successfully')
        
        # Verify user was created correctly
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_register_user_invalid_data(self):
        """Test user registration with invalid data."""
        invalid_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': '123'
        }
        response = self.client.post('/api/users/register/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)
    
    def test_register_user_duplicate_username(self):
        """Test user registration with duplicate username."""
        User.objects.create_user(
            username='testuser',
            email='existing@example.com',
            password='pass123'
        )
        response = self.client.post('/api/users/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_register_user_duplicate_email(self):
        """Test user registration with duplicate email."""
        User.objects.create_user(
            username='existinguser',
            email='test@example.com',
            password='pass123'
        )
        response = self.client.post('/api/users/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_get_profile_authenticated(self):
        """Test getting user profile when authenticated."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertNotIn('password', response.data)
    
    def test_get_profile_unauthenticated(self):
        """Test getting user profile when not authenticated."""
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_profile_data_structure(self):
        """Test that profile response contains expected fields."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/users/profile/')
        expected_fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        for field in expected_fields:
            self.assertIn(field, response.data)
        self.assertNotIn('password', response.data)
