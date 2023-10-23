# Generated by Django 4.2.4 on 2023-10-21 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_profile_first_name_profile_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='surname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='По батькові'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Прізвище'),
        ),
    ]
