from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
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
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Користувач')
    phone_number = PhoneNumberField(
        default='', blank=True, verbose_name='Номер')
    department = models.CharField(
        'Стать', choices=DEPART, blank=True, null=True)
    city = models.CharField('Місто', blank=True,  max_length=100)
    first_name = models.CharField('Ім\'я', max_length=150, blank=True)
    last_name = models.CharField('Прізвище', max_length=150, blank=True)
    adress = models.CharField('Адресса', blank=True, max_length=100)
    surname = models.CharField(
        "По батькові",  blank=True, max_length=50)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профіль'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
