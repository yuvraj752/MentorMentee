from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("video-call/", views.VideoCall.as_view(), name='video-call'),
    path("register/", views.UserCreate.as_view(), name='register'),
    path("login/", views.Login.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
]
