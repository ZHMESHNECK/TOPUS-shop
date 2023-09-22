from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from rest_framework.generics import GenericAPIView
from users.serializers import *
from users.forms import UserRegistrationForm, LoginUserForm
from users.models import User
import requests


class ActivateUser(GenericAPIView):

    def get(self, request, uid, token, format=None):
        payload = {"uid": uid, "token": token}

        url = "http://localhost:8000/api/auth/users/activation/"
        response = requests.post(url, json=payload)

        if response.status_code in (204, 301, 302):
            return redirect('/')
        else:
            print('error')
            # return redirect('error')


class RegisterView(CreateView):
    """Сторінка реєстрації нового користувача
    """
    queryset = User.objects.all()
    form_class = UserRegistrationForm
    serializer_class = UserCreateSerializer
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Реєстрація'
        return context

    def post(self, request, *args, **kwargs):

        form = UserRegistrationForm(request.POST)

        data = {"email": "", "username": "", "password": "", "re_password": ""}
        data["email"] = request.POST['email']
        data["username"] = request.POST['username']
        data["password"] = request.POST['password']
        data["re_password"] = form.clean_password2()
        url = 'http://localhost:8000/api/auth/users/'
        response = requests.post(url, data=data)
        if response.status_code == 400:
            form.error_400(response.content.decode())

            parametrs = {
                "email": data['email'],
                "username": data['username'],
                "password": "",
                "re_password": "",
                "form": form
            }
            return render(request, 'register.html', parametrs)
        return redirect('success_registration')


class EmailSentView(TemplateView):

    template_name = 'success_register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Лист активації відправлено'
        return context


class LoginUser(LoginView):
    serializer_class = UserLoginSerializer
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вхід'
        return context


def logout_user(request):
    logout(request)
    return redirect('/')
