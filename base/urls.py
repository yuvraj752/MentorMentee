from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import SetPasswordForm

urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path("register/", views.Register.as_view(), name='register'),
    path("login/", views.Login.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'), name='password_reset'
    ),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'
    ),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html', form_class=SetPasswordForm
        ), name='password_reset_confirm'
    ),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'
    ),
    path("mentor_search", views.MentorSearch.as_view(), name='mentor_search'),
    path("mentor_detail/<slug>", views.MentorDetail.as_view(), name='mentor_detail'),
    path("mentor_form/<pk>", views.MentorForm.as_view(), name='mentor_form'),
    path("chat/<chat_room>", views.ChatList.as_view(), name='chat'),
    path("chat_room_list/", views.ChatRoomList.as_view(), name='chat_room_list'),
]
