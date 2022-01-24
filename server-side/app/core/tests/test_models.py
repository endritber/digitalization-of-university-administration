from multiprocessing.sharedctypes import Value
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='student@university.com', password='student12345'):
    """Create a sample user for authorization"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful
        """
        email = 'test@gmail.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
            role = 1
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        """
        email = 'test@gmail.com'
        user = get_user_model().objects.create_user(email, 'test123')
        
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating user with no email raises error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """
        Creating a new superuser
        """
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_progress_str(self):
        """Test the progress string representation"""
        progress = models.Progress.objects.create(
            user=sample_user(),
            department='CSE',
            level='Bachelor'
        )
        self.assertEqual(str(progress), progress.user.email + " | Academic Progress")

    def test_transcript_student_created(self):
        """Test that a transcript is created when a progress is created"""
        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            name='test123',
            role=1
        )
        progress = models.Progress.objects.create(
            user=user,
            department='CSE',
            level='Bachelor'
        )
        transcript = models.Transcript.objects.get(user=user)
        self.assertEqual(str(transcript), transcript.user.email + "'s Transcript")
    
    def test_grade_added_to_progress(self):
        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            name='test123',
            role=3
        )
        progress = models.Progress.objects.create(
            user=user,
            department='CSE',
            level='Bachelor'
        )

        course = models.Course.objects.create(
            course_code = 'code',
            course_name = 'course',
            ects = 5,
            category='Obligative'
        )
        grade = models.CourseGrade.objects.create(
            grade = 10,
            course = course,
            user = user
        )
        transcript = models.Transcript.objects.get(user=user)
        the_grade = transcript.grade_courses.all()
        self.assertIn(grade, the_grade)
