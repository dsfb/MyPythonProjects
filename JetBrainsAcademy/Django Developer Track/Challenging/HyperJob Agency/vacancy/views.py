from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import VacancyForm
from .models import Vacancy


def vacancy_list(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'vacancy_list.html', {'vacancies': vacancies})


def vacancy_new(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    if not request.user.is_staff:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')

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
