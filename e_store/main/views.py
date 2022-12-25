from django.shortcuts import render, redirect
from .forms import LoginForm


def main_page(request):
    return render(request, "main/index.html")


def login_page(request):
    form = LoginForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'main/login.html', context)
