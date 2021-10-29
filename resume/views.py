from django.shortcuts import render
from django.views import View
from resume.models import Resume

# Create your views here.


class Resumes(View):
    def get(self, request, *args, **kwargs):
        context = {'resume_lst': Resume.objects.all()}
        return render(request, 'resume/resume_lst.html', context=context)
