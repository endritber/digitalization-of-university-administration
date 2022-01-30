from django.db import IntegrityError, models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.conf import settings
from django.forms import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, date_of_birth=None,
    phone_number=None, gender=None, identity_card_number=None, parent_name=None,
    place_of_birth=None, address=None, country=None, nationality=None, settlement=None, **extra_fields):
        """
        Creates and saves a new user
        """
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), role=role,date_of_birth=date_of_birth,
                 phone_number=phone_number, gender=gender, identity_card_number=identity_card_number, parent_name=parent_name,
                 place_of_birth=place_of_birth, address=address, country=country, nationality=nationality, settlement=settlement, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a new superuser
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username
    """
    ADMINISTRATOR = 1
    PROFESSOR = 2
    STUDENT = 3

    ROLE_CHOICES = (
        (ADMINISTRATOR, 'Administrator'),
        (PROFESSOR, 'Professor'),
        (STUDENT, 'Student')
    )
    GENDER_CHOICE = (
        ('M', 'M'),
        ('F', 'F')
    )

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    identity_card_number = models.IntegerField(null=True, blank=True)
    parent_name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=255)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=255, null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    settlement = models.CharField(max_length=255, blank=True,null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to='profile', null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Course(models.Model):
    """Course Model"""
    course_code = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    ects = models.PositiveIntegerField(validators=[MinValueValidator(2), MaxValueValidator(6)])
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.course_code + ' | '+self.course_name


class CourseGrade(models.Model):
    """CourseGrade Model"""
    grade = models.PositiveIntegerField(validators=[MinValueValidator(5), MaxValueValidator(10)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email + " | "+str(self.grade) + " | "+self.course.course_name

    def save(self,*args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        if created:
            try:
                t = Transcript.objects.get(user=self.user)
                t.grade_courses.add(CourseGrade.objects.get(id=self.id))
                t.save()
            except:
                raise ValidationError('You are trying to add a grade to a student without transcript or to a non student. \
                      Make sure the administrator has added an academic progress for this student.')


class Transcript(models.Model):
    """Transcript model"""
    grade_courses = models.ManyToManyField(CourseGrade, related_name='grade_courses', blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.email + "'s Transcript"


class Examination(models.Model):
    """Examination model"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.course_name + "|" + self.user.name


class Progress(models.Model):
    """Progress to be used for a student"""
    level = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    transcript = models.OneToOneField(Transcript, on_delete=models.CASCADE, null=True, blank=True)
    exams = models.ManyToManyField(Examination, related_name='progress', blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    )
    def save(self,*args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        if created:
            try:
                t = Transcript.objects.create(user=self.user)
                t.save()
                p = Progress.objects.get(id=self.id)
                p.transcript = Transcript.objects.get(user=self.user)
                p.save()
            except IntegrityError:
                pass

    def __str__(self):
        return self.user.email + " | Academic Progress"