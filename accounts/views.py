# [accounts/views.py]
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, RegisterForm


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        from django.urls import reverse
        return reverse('dashboard')


def user_logout(request):
    """Logout view that redirects to login page"""
    logout(request)
    return redirect('accounts:login')


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

