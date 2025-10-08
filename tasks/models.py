from django.db import models
from django.conf import settings

class Task(models.Model):
    """Tasks model """
    PRIORITY_CHOICES = [
        (1, "Lowest"),
        (2, "Low"),
        (3, "Medium"),
        (4, "High"),
        (5, "Critical"),
    ]

    REMINDER_CHOICES = [
        (1, "None"),
        (2, "1 hour"),
        (3, "30 minutes"),
        (4, "10 minutes"),
    ]

    STATUS_CHOICES = [
        (1, "Pending"),
        (2, "Done"),
        (3, "Failed"),
    ]

    title = models.CharField(max_length=50)
    description = models.TextField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    deadline = models.DateTimeField()
    local_deadline = models.DateTimeField(blank=True, null=True)
    reminder = models.IntegerField(choices=REMINDER_CHOICES, default=1)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    celery_task_failed = models.CharField(max_length=255, blank=True, null=True)
    celery_task_reminder = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
    
class Reminding(models.Model):
    """Remindings model"""
    task_title = models.CharField(max_length=50)
    time_left = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_title
