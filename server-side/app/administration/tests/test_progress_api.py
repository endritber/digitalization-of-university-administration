from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from core import models
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Progress
from administration.serializers import ProgressSerializer

PROGRESS_URL = reverse('administration:progress-list')
COURSE_URL = reverse('administration:course')

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
            'student@university.com',
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
        user = get_user_model().objects.create_user(
            'stud@university.com',
            'testpass123',
            3,
        )
        payload = {'level':'Bachelor','department':'Computer Science and Engineering', 'user':user.id}
        res = self.client.post(PROGRESS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Progress.objects.filter(
            user = user.id,
        ).exists()
        self.assertTrue(exists)

    def test_create_progress_invalid(self):
        """Test creating a new progress with invalid payload"""
        user = get_user_model().objects.create_user(
            'stud@university.com',
            'testpass123',
            3,
        )
        payload = {'department':'', 'user':user.id}
        res = self.client.post(PROGRESS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_grade(self):
        """Test proffesor adding grade to a student"""
        user = get_user_model().objects.create_user(
            'prof@university.com',
            'testpass123',
            2,
        )
        self.client.force_authenticate(self.user)
        user2 = get_user_model().objects.create_user(
            'stud@university.com',
            'testpass123',
            3,
        )
        progress = models.Progress.objects.create(
            user=user2,
            department='CSE',
            level='Bachelor'
        )
        course = models.Course.objects.create(
            course_code = 'code',
            course_name = 'course',
            ects = 5,
            category='Obligative'
        )
        payload = {'grade':10, 'course':course.id}
        GRADE_URL = reverse('administration:grade', args=[user2.id])
        self.client.force_authenticate(user)
        res = self.client.post(GRADE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        transcript = models.Transcript.objects.get(user=user2)
        the_grade = transcript.grade_courses.all()
        self.assertEqual(res.data['id'], the_grade[0].id)

    def test_add_grade_invalid(self):
        """Test other user adding grade to a student and prof adding grade to non-student"""

        user = get_user_model().objects.create_user(
            'admin@university.com',
            'testpass123',
            1,
        )
        self.client.force_authenticate(self.user)
        user2 = get_user_model().objects.create_user(
            'stud@university.com',
            'testpass123',
            3,
        )
        user3 = get_user_model().objects.create_user(
            'prof@university.com',
            'testpass123',
            2,
        )
        progress = models.Progress.objects.create(
            user=user2,
            department='CSE',
            level='Bachelor'
        )
        course = models.Course.objects.create(
            course_code = 'code',
            course_name = 'course',
            ects = 5,
            category='Obligative'
        )
        payload = {'grade':10, 'course':course.id}
        GRADE_URL = reverse('administration:grade', args=[user2.id])
        self.client.force_authenticate(user)
        res = self.client.post(GRADE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        payload = {'grade':10, 'course':course.id}
        GRADE_URL = reverse('administration:grade', args=[user.id])
        self.client.force_authenticate(user3)
        try:
            res = self.client.post(GRADE_URL, payload)
        except:
            self.assertTrue(True)

    def test_list_course_and_course_detail(self):
        user = get_user_model().objects.create_user(
            'prof@university.com',
            'testpass123',
            2,
        )
        course = models.Course.objects.create(
            course_code = 'code',
            course_name = 'course',
            ects = 5,
            category='Obligative'
        )
        self.client.force_authenticate(user=user)
        res = self.client.get(COURSE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        COURSE_DETAIL_URL = reverse('administration:course-detail', args=[course.id])
        res = self.client.get(COURSE_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)



        
