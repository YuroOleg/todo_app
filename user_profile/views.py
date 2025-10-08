from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.decorators import login_required

@login_required(login_url='register')
def profile(request):
    """Profile view"""

    profile = Profile.objects.get(user=request.user)

    return render(request, 'user_profile/profile.html', {'profile': profile})

@login_required(login_url='register')
def edit_profile(request):
    """View of profile editing"""

    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile_picture_path = request.FILES.get('profile_picture')

        
        profile.bio = bio
        if profile_picture_path:
            profile.profile_picture = profile_picture_path
        profile.save()
        return redirect('profile')


    return render(request, 'user_profile/edit_profile.html', {'profile': profile})
