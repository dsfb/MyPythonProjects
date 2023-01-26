from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView


class UserCreateView(CreateView):
    form_class = UserCreationForm
    success_url = "/schedule/main"
    template_name = 'schedule/signup.html'


class UserLoginView(LoginView):
    model = User
    fields = ['username', 'password']
    success_url = "/schedule/main"
    template_name = 'schedule/login.html'