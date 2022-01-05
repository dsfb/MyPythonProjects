from django import http
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .forms import VacancyForm
from .models import Vacancy


# Create your views here.
def vacancy_list(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'vacancy_list.html', {'vacancies': vacancies})


def vacancy_new(request):
    if not request.user.is_authenticated:
        raise PermissionDenied()

    if request.method == 'POST':
        post_dict = request.POST
        vacancy = Vacancy()
        vacancy.author = request.user
        vacancy.description = post_dict['description']
        vacancy.save()
        return redirect('home')
    else:
        # GET request
        form = VacancyForm()
        return render(request, 'vacancy_new.html', {'form': form})

    return None
