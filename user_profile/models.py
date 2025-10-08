from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    """Profile model"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/profile_picture_placeholder.png')
    bio = models.TextField(blank=True)
    tasks_complete = models.IntegerField(default=0)
    tasks_failed = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username
