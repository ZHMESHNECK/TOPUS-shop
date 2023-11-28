from phonenumber_field.phonenumber import PhoneNumber
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import renderers, status
from django.contrib.auth.views import *
from django.contrib.auth import logout
from django.views.generic.edit import FormView
from django.views.generic import CreateView, TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError
from django.http import Http404
from users.serializers import *
from users.permission import *
from users.models import User
from users.forms import *
import requests
import traceback


# from django.contrib.auth.views import LoginView - need test !!!!!
class ActivateUser(GenericAPIView):

    def get(self, request, uid, token, format=None):
        payload = {"uid": uid, "token": token}

        url = "http://localhost:8000/api/auth/users/activation/"
        response = requests.post(url, json=payload)

        if response.status_code in (204, 301, 302):
            messages.success(
                request, 'Профіль створено, тепер можете увійти')
            return redirect('home', permanent=True)
        else:
            messages.error(
                request, 'При створенні профілю сталася помилка')
            return render(request, '404.html')


class ChangePasswordUser(PasswordContextMixin, FormView):
    """Сторінка вводу нового пароля
    """
    form_class = SetPasswordForm
    template_name = 'make_new_pass.html'
    title = 'Зміна пароля'

    def post(self, request, *args, **kwargs):
        form = SetPasswordForm(request.POST)

        data = {"uid": kwargs['uidb64'], "token": kwargs['token'], "new_password": request.POST['new_password'],
                "re_new_password": request.POST['re_new_password']}

        url = 'http://localhost:8000/api/auth/users/reset_password_confirm/'
        response = requests.post(url, data=data)
        if response.status_code != 204:
            form.error_400(response.content.decode())
            parametrs = {
                "new_password": "",
                "re_new_password": "",
                "form": form
            }
            return render(request, self.template_name, parametrs)
        messages.success(request, 'Пароль успішно змінено')
        return redirect('home')


class ForgotPassword(PasswordResetView):
    """Сторінка вводу пошти для зміни пароля
    """
    form_class = ForgotPasswordForm
    template_name = 'send_change_pass.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Змінити пароль'
        return context

    def post(self, request, *args, **kwargs):
        try:
            data = {"email": request.POST['email']}
            url = 'http://localhost:8000/api/auth/users/reset_password/'
            response = requests.post(url, data=data)
            if response.status_code != 204:
                return render(request,  '404.html')
            messages.info(
                request, 'На пошту було відправлено лист для зміни пароля')
            return redirect('home')
        except:
            messages.error(request, 'Сталася помилка :(')
            return render(request, template_name=self.template_name)


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

        data = {"email": request.POST['email'], "username": request.POST['username'],
                "password": request.POST['password'], "re_password": form.clean_password2()}
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
            return render(request, self.template_name, parametrs)
        messages.info(
            request, 'На пошту було відправлено лист для підтвердження реєстрації')
        return redirect('home')


class EmailSendView(TemplateView):

    template_name = 'success_register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Лист активації відправлено'
        return context


class LoginUser(LoginView):
    """Сторінка логіну
    """
    serializer_class = UserLoginSerializer
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вхід'
        return context


def logout_user(request):
    logout(request)
    return redirect('/')


class ProfileViewSet(ModelViewSet):
    """Сторінка відображення профіля юзера
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly, IsStaffOrReadOnly]
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def list(self, request):
        return Response(template_name='404.html', data={'message': 'Упс, цієї сторінки не існує'}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk: str = None):
        # pk = username
        try:
            user = self.queryset.get(user__username=pk)
            if user.user_id != request.user.id:
                raise Http404
        except:
            return Response(template_name='404.html', data={'message': 'Упс, цієї сторінки не існує'}, status=status.HTTP_404_NOT_FOUND)
        if request.accepted_renderer.format == 'html':
            form = ProfileForm(
                initial={'phone_number': user.phone_number}, instance=user)  # phone / department
            return Response({'profile': user, 'form': form}, template_name='user_profile.html')

        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """ Зберігає персональні данні

        Args:
            request (_type_): _description_

        Returns:
            Response: data=dict
        """
        profile = self.queryset.get(user_id=request.user.id)
        data = request.data

        # Зберігання даних з кошика
        if request.data.get('cart'):
            try:
                profile.first_name = data.get('first_name')
                profile.last_name = data.get('last_name')
                profile.surname = data.get('surname')
                number = PhoneNumber.from_string(
                    data.get('phone_number_1'), region=data.get('phone_number_0'))
                profile.phone_number = number
                profile.save()
                messages.success(request, 'Данні успішно збережено')
                return Response(status=status.HTTP_202_ACCEPTED)
            except:
                messages.error(request, 'Сталася помилка')
                return Response(status=status.HTTP_400_BAD_REQUEST)

        # Зберігання даних з профілю
        else:
            try:
                if profile.user.username != data.get('username'):
                    user = profile.user
                    user.username = data.get('username')
                    user.save()

                profile.first_name = data.get('first_name')
                profile.last_name = data.get('last_name')
                profile.surname = data.get('surname')
                number = PhoneNumber.from_string(
                    data.get('phone_number_1'), region=data.get('phone_number_0'))
                profile.phone_number = number
                profile.department = data.get('department')
                profile.city = data.get('city')
                profile.adress = data.get('adress')
                profile.save()
                profile.refresh_from_db()
                messages.success(request, 'Данні успішно збережено')
                return Response(data={'username': profile.user.username}, status=status.HTTP_202_ACCEPTED)
            except IntegrityError:
                messages.error(request, 'Юзер з таким нікнеймом вже існує')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                messages.error(request, 'Сталася помилка')
                return Response(status=status.HTTP_400_BAD_REQUEST)
