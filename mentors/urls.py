from django.urls import path
from . import views

urlpatterns = [
    path("mentor_search", views.MentorSearch.as_view(), name='mentor_search'),
    path("mentor_detail/<slug>", views.MentorDetail.as_view(), name='mentor_detail'),
    path("mentor_form/<pk>", views.MentorFormView.as_view(), name='mentor_form'),
]