from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("message-list/<pk>", views.MessageList.as_view(), name='message-list'),
    path("message-detail/<pk>", views.MessageDetail.as_view(), name='message-detail'),
    path("message-create/<pk>", views.MessageCreate.as_view(), name='message-create'),
    path("message-reply/<pk>", views.MessageReply.as_view(), name='message-reply'),
    path("video-call/", views.VideoCall.as_view(), name='video-call'),
    path("register/", views.UserCreate.as_view(), name='register'),
    path("login/", views.Login.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
]
