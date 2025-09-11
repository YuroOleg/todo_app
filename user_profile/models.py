from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="images/", blank=True, null=True, default="images/default.png")
    bio = models.TextField(blank=True, null=True)
    tasks_done = models.IntegerField(default=0)
    tasks_overdue = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
