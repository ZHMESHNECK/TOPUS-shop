# Generated by Django 4.2.4 on 2023-10-22 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile_surname_alter_profile_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
    ]
