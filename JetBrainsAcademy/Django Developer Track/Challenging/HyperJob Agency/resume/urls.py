from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.resume_list, name="index"),
    url(r'^new$', views.resume_new, name="new"),
]