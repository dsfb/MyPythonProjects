from django.conf.urls import url
from . import views

urlpatterns = [
    url('vacancies', views.vacancy_list, name="index"),
    url('vacancy/new', views.vacancy_new, name="new"),
]