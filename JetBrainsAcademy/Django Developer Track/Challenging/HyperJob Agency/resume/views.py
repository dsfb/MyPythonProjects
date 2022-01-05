from django import http
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import Resume


# Create your views here.
def resume_list(request):
    resumes = Resume.objects.all()
    return render(request, 'resume_list.html', {'resumes': resumes})


def resume_new(request):
    if not request.user.is_authenticated:
        raise PermissionDenied()

    if request.method == 'POST':
        post_dict = request.POST
        resume = Resume()
        resume.author = request.user
        resume.description = post_dict['description']
        resume.save()
        return redirect('home')
    else:
        form = ResumeForm()
        return render(request, 'resume_new.html', {'form': form})

    return None
