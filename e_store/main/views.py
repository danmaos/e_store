from django.shortcuts import render, redirect
from .forms import LoginForm, OrderForm, CommentForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from .models import Goods, Comment, Review
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .filters import ProductFilter


def main_page(request):
    goods = Goods.objects.all()
    review = Review.objects.all()
    form = ReviewForm(initial={'user': request.user})
    if request.method == 'POST':
        form = ReviewForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.review = review
            form.save()
    filter = ProductFilter(request.GET, queryset=goods)
    goods = filter.qs
    context = {'goods': goods, 'review': review, 'form': form, 'filter': filter}
    return render(request, "main/index.html", context)


def average_rate(rates):
    total = 0
    count = 0
    for i in rates:
        total += i.rate
        count += 1
    if count != 0:
        return round(total / count)
    else:
        return 'No rating yet'


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
    comment = good.comment_set.all()
    rates = good.rating_set.all()
    result = average_rate(rates)
    form = CommentForm(initial={'good': good})
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.good = good
            form.save()
    context = {'good': good, 'comment': comment, 'form': form, 'rates': result}
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


def product_list(request):
    good = Goods.objects.all()
    paginator = Paginator(good, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'good': good, 'page_obj': page_obj}
    return render(request, 'main/product_list.html', context)



