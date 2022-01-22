from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Progress
from administration.serializers import ProgressSerializer

PROGRESS_URL = reverse('administration:progress-list')

class PublicProgressApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving progress of a student"""
        res = self.client.get(PROGRESS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateProgressApiTests(TestCase):
    """Test the authorized user tags API"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@university.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_progress(self):
        """Test retrieve student progress"""
        Progress.objects.create(user=self.user, degree='Bachelor')
        res = self.client.get(PROGRESS_URL)
        progress = Progress.objects.all()
        serializer = ProgressSerializer(progress, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_progress_limited_to_user(self):
        """Test that progress returned for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'testpass123'
        )
        Progress.objects.create(user=user2, degree='Master')
        progress = Progress.objects.create(user=self.user, degree='Bachelor')
        print(progress)
        res = self.client.get(PROGRESS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['degree'], progress.degree)

