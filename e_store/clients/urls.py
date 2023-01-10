from django.urls import path, reverse_lazy
from . import views
from django.views.generic.edit import CreateView


urlpatterns = [
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('create_profile', views.create_profile, name='create_profile'),
]