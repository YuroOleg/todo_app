from celery import shared_task
from django.utils import timezone
from datetime import datetime
from .models import Task

@shared_task
def update_overdue_tasks():
    now = datetime.now()
    print(now)
    overdue_tasks = Task.objects.filter(status='Pending', deadline__lt=now)
    overdue_tasks.update(status='Overdue')