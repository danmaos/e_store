from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm


def profile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    context = {'profile': profile}
    return render(request, 'clients/profile.html', context)


def create_profile(request):
    form = ProfileForm(initial={'user': request.user})
    if request.method == 'POST':
        form = ProfileForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect('main')
    context = {'form': form}
    return render(request, 'clients/create_profile.html', context)


def update_profile(request):
    user = request.user.profile
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('main')
    context = {'form': form}
    return render(request, 'clients/update_profile.html', context)