from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm


def profile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    context = {'profile': profile}
    return render(request, 'clients/profile.html', context)


def create_profile(request):
    form = ProfileForm(request.POST)
    context = {'form': form}
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'clients/create_profile.html', context)