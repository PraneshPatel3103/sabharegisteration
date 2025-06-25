
from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_register),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('logout/', views.logout_view, name='logout'),
]

