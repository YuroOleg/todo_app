from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import pytz


class UserManager(BaseUserManager):
    """Handles creating users and superusers of custom User model"""

    def create_user(self, username, email, password=None):
        
        if not email:
            raise ValueError("user must have email")
        if not password:
            raise ValueError("User must have a password")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
        
    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True


        user.save(using=self._db)
        return user
        



class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model for authorization"""

    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    timezone = models.CharField(max_length = 32, choices =[(tz, tz) for tz in pytz.all_timezones], default='UTC')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username
    