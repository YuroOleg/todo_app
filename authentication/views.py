from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from . import forms
# Create your views here.
def registration(request):
    if request.method == "POST":
        registration_form = forms.RegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('registration')
    else:
        registration_form = forms.RegistrationForm()
    
    return render(request, 'authentication/registration.html', {'registration_form': registration_form})

def logging_in(request):
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password = password)
            if user is not None:
                login(request, user)
                return redirect('login')
            else:
                messages.error(request, "Incorrect username or password")
                return redirect('login')
    else:
        login_form = forms.LoginForm()           

    return render(request, 'authentication/login.html', {'login_form': login_form})