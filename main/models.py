from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    PRIORITY = {
        1: "Urgent",
        2: "Important",
        3: "Medium importance",
        4: "Low importance",
        5: "Optional",
    }

    STATUS = {
        "Pending" : "Task is waiting to be done",
        "Overdue" : "Task wasn't done in time ",
        "Done" : "Task was done in time",
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.IntegerField(choices=PRIORITY)
    deadline = models.DateTimeField()
    created = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=10, choices=STATUS, default="Pending")

    def __str__(self):
        return self.title
