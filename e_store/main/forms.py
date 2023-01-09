from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, Comment


class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'quantity', 'email', 'phone', 'city', 'street', 'house', 'good', 'user', 'pay_method']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'text')