from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviewer_reporter, name='reviewer_reporter'),
]
