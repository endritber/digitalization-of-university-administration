from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch

def sample_user(email='student@university.com', password='student12345'):
    """Create a sample user for authorization"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
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
        """Test the email for a new user is normalized"""
        email = 'test@gmail.com'
        user = get_user_model().objects.create_user(email, 'test123')
        
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Creating a new superuser"""
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
        """Test grade is added to a student progress"""
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

    @patch('uuid.uuid4')
    def test_user_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.user_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/user/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)

    def test_create_new_examination(self):
        """Test examination model is created"""
        user = get_user_model().objects.create_user(
            email = 'prof@uni.net',
            password = 'test1234',
            role = 2,
            name='Prof'
        )
        course = models.Course.objects.create(course_code ='test', course_name='test', ects=5, category='test')
        models.Examination.objects.create(course=course, user=user)
        res = models.Examination.objects.get(user=user)
        self.assertEqual(str(res), str(course.course_name + "|"+user.name))
