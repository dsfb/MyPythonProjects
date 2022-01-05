"""hyperjob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.views.generic import RedirectView
from .views import HomeView, MenuView, SignupView, TheLoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MenuView.as_view(), name='menu'),
    url(r'resumes/', include('resume.urls'), name="resume"),
    url(r'resume/', RedirectView.as_view(url=r"resumes/")),
    url(r'vacancies/', include('vacancy.urls')),
    path(r'login/', RedirectView.as_view(url='login')),
    path(r'signup/', RedirectView.as_view(url='signup')),
    path(r'login', TheLoginView.as_view(), name="login"),
    path(r'signup', SignupView.as_view(), name="signup"),
    path(r'home', HomeView.as_view(), name="home"),
]
