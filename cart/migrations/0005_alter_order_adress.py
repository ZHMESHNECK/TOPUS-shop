# Generated by Django 4.2.4 on 2023-10-25 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_order_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='adress',
            field=models.TextField(blank=True, max_length=100, verbose_name='Адресса'),
        ),
    ]
