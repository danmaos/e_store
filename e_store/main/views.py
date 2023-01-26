from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import LoginForm, OrderForm, CommentForm, ReviewForm, RateForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Goods, Comment, Review
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .filters import ProductFilter
from clients.models import Profile
from .services import calculate_sale, average_rate
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def main_page(request):
    goods = Goods.objects.all()
    review = Review.objects.all()
    form = ReviewForm(initial={'user': request.user})
    if request.method == 'POST':
        form = ReviewForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.review = review
            form.save()
            return redirect(request.META['HTTP_REFERER'])
    filter = ProductFilter(request.GET, queryset=goods)
    goods = filter.qs[:3]
    for good in goods:
        if good.sale == True:
            good.price = round(good.price * 0.8)
    context = {'goods': goods, 'review': review, 'form': form, 'filter': filter}
    return render(request, "main/index.html", context)


def login_page(request):
    form = LoginForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string("main/acc_activate.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user)
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('please activate your account')
    else:
        form = LoginForm()
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
    if good.sale == True:
        good.price = round(good.price * 0.8)
    result = average_rate(rates)
    rate_form = RateForm(initial={'good':good, 'user': request.user})
    if request.method == 'POST':
        rate_form = RateForm(request.POST)
        if rate_form.is_valid():
            if 1 <= rate_form.cleaned_data['rate'] <= 5:
                rate_form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponse("you can't do it")

    form = CommentForm(initial={'good': good})
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.good = good
            form.save()
            return HttpResponse("Thank you. Your order is in process")
    context = {'good': good, 'comment': comment, 'form': form, 'rates': result, 'rate_form': rate_form}
    return render(request, 'main/product_detail.html', context)


def order(request, good_id):
    profile = Profile.objects.get(user=request.user)
    good = Goods.objects.get(id=good_id)
    form = OrderForm(initial={'good': good, 'user': request.user})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            total_price = good.price * form.cleaned_data['quantity']
            total_price = calculate_sale(profile.order_count, total_price)
            if form.cleaned_data['pay_method'] == 'visa':
                if profile.wallet >= total_price:
                    profile.wallet -= total_price
                    profile.order_count += total_price
                    profile.save()
                    return redirect(request.META['HTTP_REFERER'])
                else:
                    return HttpResponse('not enough money')
            else:
                profile.order_count += total_price
                profile.save()
                form.save()
                return redirect('main')
    context = {'good': good, 'form': form}
    return render(request, 'main/checkout.html', context)


def product_list(request):
    good = Goods.objects.all()
    paginator = Paginator(good, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'good': good, 'page_obj': page_obj}
    return render(request, 'main/product_list.html', context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Thanks for activate account")
    else:
        return HttpResponse("Activation link has crashed")