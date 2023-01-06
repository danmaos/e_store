from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('create_profile', views.create_profile, name='create_profile')
]