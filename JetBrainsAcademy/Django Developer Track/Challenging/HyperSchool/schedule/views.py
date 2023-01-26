from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentForm
from .models import Course, Teacher, Student
from django.db.models.query import QuerySet


def home(request):
    return HttpResponse("Hello home")


def main(request):
    courses: QuerySet
    query = request.GET.get('q')
    if query is None:
        courses = Course.objects.all()
    else:
        courses = Course.objects.all().filter(title__contains=query)

    context = {
        'courses': courses
    }

    return render(request, 'schedule/main.html', context)


def course_details(request, course_id):
    course = Course.objects.get(id=course_id)
    teachers = course.teacher.all()

    context = {
        'course': course,
        'teachers': teachers
    }

    return render(request, 'schedule/course_details.html', context)


def teacher_details(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)

    context = {
        'teacher': teacher
    }

    return render(request, 'schedule/teacher_details.html', context)


def __get_query_parameter(request, query_parameter):
    return request.GET.get(query_parameter)


def add_course(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            stud = form.save(commit=False)
            stud.save()
    form = StudentForm()
    return render(request, "schedule/add_course.html",
                  {"form": form})
