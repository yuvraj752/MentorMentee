from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import SetPasswordForm

urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path("chat/", views.Chat.as_view(), name='chat'),
    path("video_call/", views.VideoCall.as_view(), name='video_call'),
    path("register/", views.Register.as_view(), name='register'),
    path("login/", views.Login.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='base/auth/password_reset.html'), name='password_reset'),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='base/auth/password_reset_done.html'), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='base/auth/password_reset_confirm.html', form_class=SetPasswordForm), name='password_reset_confirm'),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name='base/auth/password_reset_complete.html'), name='password_reset_complete'),
]
