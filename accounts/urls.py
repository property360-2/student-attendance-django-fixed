# [accounts/urls.py]
from django.urls import path

from .views import RegisterView, UserLoginView, user_logout

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]

