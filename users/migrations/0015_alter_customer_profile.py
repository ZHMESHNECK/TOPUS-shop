# Generated by Django 4.2.4 on 2023-10-24 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_remove_customer_adress_remove_customer_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile',
            field=models.ForeignKey(blank=True, default='Anonymous', null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile', verbose_name='Покупець'),
        ),
    ]