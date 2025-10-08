from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def register_user(request):
    """User registration view"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            timezone = request.POST.get('timezone')
            if timezone:
                user.timezone = timezone

            user.save()
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'authorization/register.html', {'form': form})

def login_user(request):
    """User authentication view"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user

            timezone = request.POST.get('timezone')
            if timezone and user.timezone != timezone:
                user.timezone = timezone
                user.save()

            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
            
    return render(request, 'authorization/login.html', {'form': form})

@login_required(login_url='register')
def logout_user(request):
    """Logout view"""
    
    if request.method == "POST":
        logout(request)

    return render(request, 'authorization/logout.html')