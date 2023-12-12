# Generated by Django 4.2.4 on 2023-11-16 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_customer_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='adress',
            field=models.CharField(blank=True, max_length=100, verbose_name='Адреса'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.CharField(blank=True, choices=[('---', '---'), ('Жіноча', 'Жіноча'), ('Чоловіча', 'Чоловіча')], null=True, verbose_name='Стать'),
        ),
    ]