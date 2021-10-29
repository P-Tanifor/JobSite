from django.shortcuts import render, redirect
from django.views import View
from vacancy.models import Vacancy
from resume.models import Resume
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
import django
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User


# Create your views here.


class MainPage(View):
    def get(self, request, *args, **kwargs):
        # from django.contrib.auth import get_user_model
        # User = get_user_model()
        # User.objects.all().delete()
        return render(request, 'vacancy/main_page.html')


class Vacancies(View):
    def get(self, request, *args, **kwargs):
        context = {'vacancy_lst': Vacancy.objects.all()}
        return render(request, 'vacancy/vacancies_lst.html', context=context)


class RemoveVacancy(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'vacancy/del.html')

    def post(self, request, *args, **kwargs):
        Vacancy.objects.filter(id=request.POST.get("id")).delete()
        return redirect('/')


class UpdateVacancy(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'vacancy/update.html')

    def post(self, request, *args, **kwargs):
        Vacancy.objects.filter(id=request.POST.get('id')).update(description=request.POST.get('newDescription'))
        return redirect('/')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signUp.html'


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'login.html'


class NewVacRes(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'vacancy/vac_res_form.html')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if django.contrib.auth.models.User.is_staff:
                Vacancy.objects.create(author=request.user, description=request.POST.get('description'))
                return redirect('/')
            else:
                Resume.objects.create(author=request.user, description=request.POST.get('description'))
                return redirect('/')
        else:
            raise PermissionDenied()



