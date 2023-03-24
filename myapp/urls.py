from django.urls import path, include
from . import views
from .views import *
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index',views.index, name='index'),
    path('analyze',views.analyze, name='analyze'),
    path('register/',views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('account/',include("django.contrib.auth.urls")),
    path('',views.home, name = "home"),
    # path('',TemplateView.as_view(template_name = 'home.html')),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'registration/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
 
    ]         
 