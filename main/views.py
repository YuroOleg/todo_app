from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
# Create your views here.

def index(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    return render(request, 'main/index.html', {'tasks': tasks})

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

    return render(request, 'main/task_editing.html', {'adding_form': form})

def task_deleting(request, id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=id)
        task.delete()
        return redirect('home')
    
    return render(request, 'main/task_deleting.html')