from celery import shared_task
from .models import Task, Reminding
from django.core.mail import send_mail
from user_profile.models import Profile

@shared_task
def task_failed(task_id):
    task = Task.objects.get(id=task_id)
    task.status = 3
    task.save()

    profile = task.user.profile
    profile.tasks_failed += 1
    profile.save()

    

@shared_task
def send_reminding(task_id):
    task = Task.objects.get(id=task_id)
    
    reminding = Reminding()
    reminding.task_title = task.title
    reminding.user = task.user

    if task.reminder == 2:
        reminding.time_left = "1 hour"
    elif task.reminder == 3:
        reminding.time_left = "30 minutes"
    elif task.reminder == 4: 
        reminding.time_left = "10 minutes" 
    reminding.save()

    
    subject = f'Reminder! The deadline for the task "{task.title}" is approaching'
    message = f'Hello, {task.user.username}!\n\n' \
                  f'Task "{task.title}" still waits to be done, you have {reminding.time_left} left'


    send_mail(
            subject,
            message,
            None,  
            [task.user.email],
            fail_silently=False,
        )
    
