from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Profile

# Create your views here.
@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        if request.POST.get('form') == 'bio':
            bio = request.POST.get('bio')
            profile = Profile.objects.get(user=request.user)
            profile.bio = bio
            profile.save()
        elif request.POST.get('form') == 'pic':
            image = request.FILES.get("image")
            if image:
                profile = Profile.objects.get(user=request.user)
                profile.profile_image = image
                profile.save()
        elif request.POST.get('form') == 'logout':
            logout(request)
            return redirect('login')

    return render(request, 'user_profile/profile.html')