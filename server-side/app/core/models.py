from re import A
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                         BaseUserManager, PermissionsMixin)
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, date_of_birth =None,
    phone_number = None,
    gender = None,
    city = None, **extra_fields):
        """
        Creates and saves a new user
        """
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), role=role,date_of_birth=date_of_birth, phone_number=phone_number, gender=gender,city=city, **extra_fields)
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
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=255)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'


class Progress(models.Model):
    """Progress to be used for a student"""
    degree = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.name
