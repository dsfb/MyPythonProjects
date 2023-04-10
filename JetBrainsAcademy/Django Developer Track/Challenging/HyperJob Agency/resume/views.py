import sys

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from .forms import ResumeForm
from .models import Resume


class ResumeSingleton:
    _instance = None

    def __init__(self):
        self.resumes = list(Resume.objects.all())

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_resumes(cls):
        return cls.instance().resumes

    @classmethod
    def add_resume(cls, resume):
        cls.instance().resumes.append(resume)


def resume_new(request):
    if not request.user.is_authenticated:
        print("Raising PermissionDenied at resume_new!", file=sys.stderr)
        raise PermissionDenied()

    if request.method == 'POST':
        post_dict = request.POST
        resume = Resume()
        resume.author = request.user
        resume.description = post_dict.get('description', '')
        resume.save()
        ResumeSingleton.add_resume(resume)
        return redirect('home')
    else:
        form = ResumeForm()
        return render(request, 'resume_new.html', {'form': form})

    return None


def resume_list(request):
    resumes = ResumeSingleton.get_resumes()
    return render(request, 'resume_list.html', {'resumes': resumes})
