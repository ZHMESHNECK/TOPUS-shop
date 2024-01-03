from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


class Profile(models.Model):
    """Модель профіля користувача
    """
    DEPART = (
        ('---', '---'),
        ('Жіноча', 'Жіноча'),
        ('Чоловіча', 'Чоловіча'),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Користувач')
    phone_number = PhoneNumberField(
        default='', blank=True, verbose_name='Номер')
    department = models.CharField(
        'Стать', choices=DEPART, blank=True, null=True)
    first_name = models.CharField('Ім\'я', max_length=150, blank=True)
    last_name = models.CharField('Прізвище', max_length=150, blank=True)
    surname = models.CharField(
        'По батькові', blank=True, max_length=50)
    city = models.CharField('Місто', blank=True, max_length=100)
    adress = models.CharField('Адреса', blank=True, max_length=100)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профіль'


class Customer(models.Model):
    """Модель покупця замовленого товару
    """
    profile = models.ForeignKey(
        Profile, models.SET_NULL, verbose_name='Покупець', null=True, blank=True)
    first_name = models.CharField('Ім\'я', max_length=150, blank=True)
    last_name = models.CharField('Прізвище', max_length=150, blank=True)
    surname = models.CharField(
        "По батькові", blank=True, max_length=50)
    phone_number = PhoneNumberField(blank=True, verbose_name='Номер')
    email = models.EmailField('Пошта')

    def __str__(self):
        return f'Замовник: № {self.id}'

    class Meta:
        verbose_name = 'Замовник'
        verbose_name_plural = 'Замовники'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
