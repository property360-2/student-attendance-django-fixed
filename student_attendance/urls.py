# [student_attendance/urls.py]
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .views import dashboard


def home(request):
    """Always land on login page first."""
    return redirect('accounts:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('students/', include(('students.urls', 'students'), namespace='students')),
    path('attendance/', include(('attendance.urls', 'attendance'), namespace='attendance')),
    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('', home, name='home'),
]
