from django.urls import path
from . import views

urlpatterns = [
    path("", views.MentorList.as_view(), name='mentor_list'),
    path("mentor_detail/<slug>", views.MentorDetail.as_view(), name='mentor_detail'),
    path("mentor_edit/<pk>", views.MentorEdit.as_view(), name='mentor_edit'),
]