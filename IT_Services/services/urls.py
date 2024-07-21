from django.urls import path
from .views import (home, login, register, otp, service_list, service_create,
                    service_detail, service_update, service_delete,subscribe, payment)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('otp/', otp, name='otp'),
    path('services/', service_list, name='service_list'),
    path('services/new/', service_create, name='service_create'),
    path('services/<int:pk>/', service_detail, name='service_detail'),
    path('services/<int:pk>/edit/', service_update, name='service_update'),
    path('services/<int:pk>/delete/', service_delete, name='service_delete'),
    path('services/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('payment/<str:transaction_id>/', payment, name='payment'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),


]




