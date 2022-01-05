from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.vacancy_list, name="index"),
    url('new', views.vacancy_new, name="new"),
]