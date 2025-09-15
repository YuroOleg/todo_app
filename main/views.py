from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from user_profile.models import Profile
from .forms import TaskForm
# Create your views here.

@login_required(login_url='login')
def index(request):
    user = request.user

    if request.method == 'POST':
        id = int(request.POST.get("done_button"))
        task = Task.objects.get(id=id)
        task.status = 'Done'
        profile = Profile.objects.get(user=user)
        profile.tasks_done+=1
        profile.save()
        task.save()

    
    tasks = Task.objects.filter(user=user, status='Pending').order_by("-created")
    return render(request, 'main/index.html', {'tasks': tasks})

@login_required(login_url='login')
def task_adding(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    else:
        form = TaskForm()

    return render(request, 'main/task_adding.html', {'adding_form': form})

@login_required(login_url='login')
def task_editing(request, id): 
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task)

    return render(request, 'main/task_editing.html', {'adding_form': form, 'id': task.id})

@login_required(login_url='login')
def task_deleting(request, id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=id)
        task.delete()
        return redirect('home')
    
    return render(request, 'main/task_deleting.html')