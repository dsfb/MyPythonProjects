from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name="main"),
    path('course_details/<course_id>', views.course_details, name='course_details'),
    path('teacher_details/<teacher_id>', views.teacher_details, name='teacher_details'),
    path('add_course/', views.add_course, name='add_course')
]
