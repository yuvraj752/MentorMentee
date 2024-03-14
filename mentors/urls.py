from django.urls import path
from . import views

urlpatterns = [
    path("", views.MentorList.as_view(), name='mentor-list'),
    path("mentor-detail/<pk>", views.MentorDetail.as_view(), name='mentor-detail'),
    path("mentor-edit/<pk>", views.MentorEdit.as_view(), name='mentor-edit'),
]