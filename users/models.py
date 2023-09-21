from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


class Profile(models.Model):
    """Модель профіля користувача"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунти'
