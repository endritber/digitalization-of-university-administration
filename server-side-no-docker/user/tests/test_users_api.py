from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import datetime



TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
USER_URL = reverse('user:user-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUsersApiTests(TestCase):
    """Test the users API (public)"""
    def setUp(self):
        self.user = create_user(
            email='administrator@gmail.com',
            password='testpass123',
            name='administrator',
            role=1,
            phone_number='+38349758152',
            date_of_birth = datetime.date(2001, 5, 31),
            gender='M',
            identity_card_number=1174589123,
            parent_name='Marin',
            place_of_birth='Prishtine',
            address='Aktash, Agim Ramadani B1/4',
            country='Kosove',
            nationality='Shqiptar',
            settlement='Prishtine',

        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_token_for_user(self):
        """Test that token is created for user"""
        payload = {'email':'test@gmail.com', 'password':'testpass123', 'role':1}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@gmail.com', password='testpass123', role=1)
        payload = {'email':'test@gmail.com','password': 'wrong', 'role':4}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload={'email':'test@gmail.com', 'password':'testpass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that email and passoword are required"""
        res = self.client.post(TOKEN_URL, {'email':'one', 'password':'black'})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        self.client.logout()
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """Test api request that require authentication"""
    def setUp(self):
        self.user = create_user(
            email='test@gmail.com',
            password='testpass',
            name='name',
            role=1,
            phone_number='+38349758152',
            date_of_birth = datetime.date(2001, 5, 31),
            gender='M',
            identity_card_number=1174589123,
            parent_name='Marin',
            place_of_birth='Prishtine',
            address='Aktash, Agim Ramadani B1/4',
            country='Kosove',
            nationality='Shqiptar',
            settlement='Prishtine',
            is_active=True

        )
            
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_create_valid_student_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'student@gmail.com',
            'password':'testpass123',
            'name': 'Student name',
            'role':3,
            'phone_number':'+38349758152',
            'date_of_birth':datetime.date(2001, 5, 31),
            'gender':'M',
            'identity_card_number':1174589123,
            'parent_name':'Marin',
            'place_of_birth':'Prishtine',
            'address':'Aktash, Agim Ramadani B1/4',
            'country':'Kosove',
            'nationality':'Shqiptar',
            'settlement':'Prishtine',
            'is_active':True,
        }

        res = self.client.post(USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(id=res.data['id'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""
        payload = {
            'email': 'test12345@gmail.com',
            'password':'testpass',
            'name': 'Test name',
            'role':1
        }
        create_user(**payload)
        self.client.post(USER_URL, payload)
        self.assertRaises(IntegrityError)

    def test_user_password_length(self):
        """Test that password must be more than 8 characters"""
        payload = {
            'email': 'test123@gmail.com',
            'password':'test',
            'name': 'Test name',
            'role':1
        }
        res = self.client.post(USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']

        ).exists()
        self.assertFalse(user_exists)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'id':self.user.id,
            'email':self.user.email,
            'name':self.user.name,
            'role':self.user.role,
            'date_of_birth':self.user.date_of_birth.isoformat(),
            'phone_number':self.user.phone_number,
            'gender':self.user.gender,
            'identity_card_number':self.user.identity_card_number,
            'parent_name':self.user.parent_name,
            'place_of_birth':self.user.place_of_birth,
            'address':self.user.address,
            'country':self.user.country,
            'nationality':self.user.nationality,
            'settlement':self.user.settlement,
            'is_active':self.user.is_active,
        })
    
    def test_post_me_not_allowed(self):
        """Test that post is not allowed on any url"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name':'new name', 'password':'newpassword'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_student_users_profiles(self):
        """Test listing all the students profile"""
        user = create_user(email='eb44780@uni.net', password='test12345', name='endrit', role=2)
        self.client.force_authenticate(user=user)
        res = self.client.get(USER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_detailed_student_profile(self):
        """Test for getting a detailed professor"""
        user = create_user(email='prof@uni.net', password='test12345', name='endrit', role=2)
        USER_URL_DETAIL = reverse('user:user-detail', args=[user.id])
        res = self.client.get(USER_URL_DETAIL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], user.email)    
        
    def test_administrator_updating_user(self):
        """Test administrator updating a user"""
        payload = {'name':'new name', 'password':'newpassword'}
        user = create_user(email='eb44780@uni.net', password='test12345', name='endrit', role=3)
        UPDATE_URL = reverse('user:user-detail', args=[user.id])
        res = self.client.get(UPDATE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res2 = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res2.status_code, status.HTTP_200_OK)

    def test_student_create_list_users(self):
        """Test student trying to create a user and student trying to list users"""
        user = create_user(email='eb44780@uni.net', password='test12345', name='endrit', role=3)
        self.client.force_authenticate(user=user)
        payload = {
            'email': 'student@gmail.com',
            'password':'testpass123',
            'name': 'Student name',
            'role':3,
            'phone_number':'+38349758152',
            'date_of_birth':datetime.date(2001, 5, 31),
            'gender':'M',
            'identity_card_number':1174589123,
            'parent_name':'Marin',
            'place_of_birth':'Prishtine',
            'address':'Aktash, Agim Ramadani B1/4',
            'country':'Kosove',
            'nationality':'Shqiptar',
            'settlement':'Prishtine',
        }
        res = self.client.post(USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.get(USER_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_student_updating_their_profile(self):
        """Test student trying to update their profile"""
        user = create_user(email='eb44780@uni.net', password='test12345', name='endrit', role=3)
        payload = {
            'email': 'student@gmail.com',
            'password':'testpass123',
            'name': 'Student name',
            'role':3,
        }
        self.client.force_authenticate(user=user)
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res2 = self.client.patch(ME_URL, payload)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_updating_others_profile(self):
        """Test student trying to update other profiles"""
        user = create_user(email='eb44780@uni.net', password='test12345', name='endrit', role=3)
        payload = {
            'email': 'student@gmail.com',
            'password':'testpass123',
            'name': 'Student name',
            'role':3,
        }
        self.client.force_authenticate(user=user)
        UPDATE_URL = reverse('user:user-detail', args=[user.id])
        res = self.client.get(UPDATE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res2 = self.client.patch(ME_URL, payload)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)