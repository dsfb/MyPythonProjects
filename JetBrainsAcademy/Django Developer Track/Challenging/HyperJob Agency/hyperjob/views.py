from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import logout


class MenuView(View):
    @staticmethod
    def get(request):
        return render(request, 'menu.html')


class TheLogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('menu')


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class TheLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'login.html'


class HomeView(View):
    @staticmethod
    def get(request):
        return render(request, 'home.html')
