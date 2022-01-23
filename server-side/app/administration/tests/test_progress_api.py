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
            'administrator@university.com',
            'password123',
            1,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_progress(self):
        """Test retrieve student progress"""
        Progress.objects.create(user=self.user, department='CSE', level='Bachelor')
        res = self.client.get(PROGRESS_URL)
        progress = Progress.objects.all()
        serializer = ProgressSerializer(progress, many=True)


        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_progress_limited_to_user(self):
        """Test that progress returned for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'administrator1@university.com',
            'testpass123',
            1,
        )
        Progress.objects.create(user=user2, level='Bachelor', department='CSE')
        progress = Progress.objects.create(user=self.user, level='Bachelor', department='CSE')
        res = self.client.get(PROGRESS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['department'], progress.department)
        self.assertEqual(res.data[0]['level'], progress.level)

    def test_create_progress_successful(self):
        """Test creating progress for a student"""
        payload = {'level':'Bachelor','department':'Computer Science and Engineering', 'user':self.user.id}
        self.client.post(PROGRESS_URL, payload)

        exists = Progress.objects.filter(
            user = self.user,
            level = payload['level'],
            department = payload['department']
        ).exists()

        self.assertTrue(exists)

    def test_create_progress_invalid(self):
        """Test creating a new progress with invalid payload"""

        payload = {'department':''}
        res = self.client.post(PROGRESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
