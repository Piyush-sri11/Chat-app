from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username=models.CharField(max_length=25)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return self.email
    
class ChatModel(models.Model):
    sender=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,  # Changed from CASCADE to SET_NULL
        related_name='sender',
        null=True,  # Allow null values
        blank=True  # Allow blank in forms
    )
    message=models.TextField(null=True, blank=True)
    thread_name=models.CharField(max_length=100,null=True, blank=True)
    timestamp=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message
    



