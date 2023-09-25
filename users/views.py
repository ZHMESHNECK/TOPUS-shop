from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import renderers
from users.forms import UserRegistrationForm, LoginUserForm
from users.serializers import *
from users.models import User
from users.permission import *
from relations.models import Relation
import requests


# https://www.django-rest-framework.org/tutorial/3-class-based-views/


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
        if not response.status_code == 201:
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


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly, IsStaffOrReadOnly]
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def retrieve(self, request, pk=None):
        try:
            response = self.queryset.get(user_id=pk)
        except:
            return render('eror')
        relation = Relation.objects.filter(user=pk)
        if len(relation) == 0:
            relation = None
        if request.accepted_renderer.format == 'html':
            return Response({'data': response,'relation': relation}, template_name='user_profile.html')
        return response
