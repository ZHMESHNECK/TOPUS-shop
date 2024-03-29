# Generated by Django 4.2.4 on 2023-10-24 09:14

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_profile_first_name_alter_profile_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='Місто')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name="Ім'я")),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='Прізвище')),
                ('adress', models.CharField(blank=True, max_length=100, verbose_name='Адресса')),
                ('surname', models.CharField(blank=True, max_length=50, verbose_name='По батькові')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Номер')),
                ('email', models.EmailField(max_length=254, verbose_name='Пошта')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Покупець', to='users.profile')),
            ],
            options={
                'verbose_name': 'Замовник',
                'verbose_name_plural': 'Замовники',
            },
        ),
    ]
