# [students/urls.py]
from django.urls import path
from .views import (
    StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView
)

urlpatterns = [
    path('', StudentListView.as_view(), name='list'),
    path('add/', StudentCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', StudentUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='delete'),
]
