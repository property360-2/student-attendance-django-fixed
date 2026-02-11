# [attendance/urls.py]
from django.urls import path
from .views import attendance_list, attendance_mark

urlpatterns = [
    path('', attendance_list, name='list'),
    path('mark/', attendance_mark, name='mark'),
]
