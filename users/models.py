from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


class Profile(models.Model):
    """Модель профіля користувача
    """
    DEPART = (
        ('Жіноча', 'Жіноча'),
        ('Чоловіча', 'Чоловіча'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(default=None, null=True, blank=True, verbose_name='Номер')
    department = models.CharField('Стать', choices=DEPART, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунти'
