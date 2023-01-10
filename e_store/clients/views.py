from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm


def profile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    context = {'profile': profile}
    return render(request, 'clients/profile.html', context)


def create_profile(request):
    form = ProfileForm(initial={'user': request.user})
    context = {'form': form}
    if request.method == 'POST':
        form = ProfileForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'clients/create_profile.html', context)