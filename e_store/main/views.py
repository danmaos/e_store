from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, OrderForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from .models import Goods, Comment
from django.utils import timezone


def main_page(request):
    goods = Goods.objects.all()
    context = {'goods': goods}
    return render(request, "main/index.html", context)


def login_page(request):
    form = LoginForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')

    return render(request, 'main/login.html', context)


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('main')
    return render(request, 'main/sign_in.html')


def logout_page(request):
    logout(request)
    return redirect('main')


def product_detail(request, good_id):
    good = Goods.objects.get(id=good_id)
    context = {'good': good}
    return render(request, 'main/product_detail.html', context)


def order(request, good_id):
    good = Goods.objects.get(id=good_id)
    form = OrderForm(initial={'good': good, 'user': request.user})
    context = {'good': good, 'form': form}
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'main/checkout.html', context)


# def comment_list(request):
#     comments = Comment.objects.filter