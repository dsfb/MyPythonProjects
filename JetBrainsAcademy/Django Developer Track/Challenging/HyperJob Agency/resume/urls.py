from django.conf.urls import url
from . import views


urlpatterns = [
    url('resumes', views.resume_list, name="index"),
    url('resume/new', views.resume_new, name="new"),
]