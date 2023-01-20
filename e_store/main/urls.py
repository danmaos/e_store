from django.urls import path
from . import views
from .views import activate

urlpatterns = [
    path('', views.main_page, name='main'),
    path('login', views.login_page, name='login'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('logout', views.logout_page, name='logout'),
    path('product/<int:good_id>', views.product_detail, name='product'),
    path('order.<int:good_id>', views.order, name='order'),
    path('product_list', views.product_list, name='product_list'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
]