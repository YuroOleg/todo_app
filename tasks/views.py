from django.shortcuts import render, redirect
from .models import Task, Reminding
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from user_profile.models import Profile
from .tasks import task_failed, send_reminding
from celery import current_app
from datetime import timedelta
from django.utils import timezone
# Create your views here.

@login_required(login_url='register')
def home(request):
    """View of main page"""
    tasks = Task.objects.filter(user = request.user, status=1).order_by('-created_at')


    if request.method == 'POST':

        task_id = request.POST.get('done')
        task = tasks.get(id=task_id)
        task.status = 2
        task.save()

        if task.celery_task_failed:
                current_app.control.revoke(task.celery_task_failed, terminate=True)

        if task.celery_task_reminder:
                current_app.control.revoke(task.celery_task_reminder, terminate=True)

        profile = task.user.profile
        profile.tasks_complete += 1
        profile.save()

        redirect('home')
    
    return render(request, 'tasks/home.html', {'tasks': tasks})

@login_required(login_url='register')
def create_task(request):
    """View for creating tasks"""
    if request.method == 'POST':
        form = TaskForm(request.POST, user = request.user)

        if form.is_valid():
            task = form.save()
            celery_task_id = task_failed.apply_async((task.id,), eta=task.deadline)
            task.celery_task_failed = celery_task_id
            task.save()

            reminder_offsets = {
                2: timedelta(hours=1),
                3: timedelta(minutes=30),
                4: timedelta(minutes=10)
            }

            if task.reminder in reminder_offsets:
                remind_time = task.deadline - reminder_offsets[task.reminder]
                if timezone.now() < remind_time:
                    task.celery_task_reminder = send_reminding.apply_async((task.id,), eta=remind_time)
                    task.save()

            return redirect('home')
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})

@login_required(login_url='register')
def edit_task(request, id):
    """View for creating tasks"""
    task = Task.objects.get(id=id)


    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user = request.user)

        if form.is_valid():
            task = form.save()
            if task.celery_task_failed:
                current_app.control.revoke(task.celery_task_failed, terminate=True)
            celery_task_id = task_failed.apply_async((task.id,), eta=task.deadline)
            task.celery_task_failed = celery_task_id
            task.save()

            if task.celery_task_reminder:
                current_app.control.revoke(task.celery_task_reminder, terminate=True)

            reminder_offsets = {
                2: timedelta(hours=1),
                3: timedelta(minutes=30),
                4: timedelta(minutes=10)
            }

            if task.reminder in reminder_offsets:
                remind_time = task.deadline - reminder_offsets[task.reminder]
                if timezone.now() < remind_time:
                    task.celery_task_reminder = send_reminding.apply_async((task.id,), eta=remind_time)
                    task.save()

            return redirect('home')
    else:
        form = TaskForm(instance=task)
        form.fields['deadline_date'].initial = task.local_deadline.date().strftime('%Y-%m-%d')
        form.fields['deadline_time'].initial = task.local_deadline.time()

    return render(request, 'tasks/edit_task.html', {'form': form})

@login_required(login_url='register')
def delete_task(request, id):
    """Task deleting view"""
    
    if request.method == 'POST':
       task = Task.objects.get(id=id)

       if task.celery_task_failed:
                current_app.control.revoke(task.celery_task_failed, terminate=True)

       if task.celery_task_reminder:
                current_app.control.revoke(task.celery_task_reminder, terminate=True)

       task.delete()


       return redirect('home')

    return render(request, 'tasks/delete_task.html')

@login_required(login_url='register')
def tasks_done(request):
    """View for list of completed tasks"""

    tasks = Task.objects.filter(user = request.user, status=2).order_by('-created_at')
    
    return render(request, 'tasks/tasks_done.html', {'tasks': tasks})

@login_required(login_url='register')
def tasks_failed(request):
    """View for list of failed tasks"""

    tasks = Task.objects.filter(user = request.user, status=3).order_by('-created_at')
    
    return render(request, 'tasks/tasks_failed.html', {'tasks': tasks})

@login_required(login_url='register')
def reminder(request):
    """Reminder view with task remindings"""

    if request.method == "POST":
        reminding_id = request.POST.get("reminding")
        Reminding.objects.get(id=reminding_id).delete()

        redirect('reminder')
        
    remindings = Reminding.objects.filter(user = request.user).order_by('-created_at')
    
    return render(request, 'tasks/reminder.html', {'remindings': remindings})
