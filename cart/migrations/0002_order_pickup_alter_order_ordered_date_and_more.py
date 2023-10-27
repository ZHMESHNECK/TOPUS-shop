# Generated by Django 4.2.4 on 2023-10-24 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pickup',
            field=models.CharField(default='-', max_length=50, verbose_name='Метод доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Прийнято', 'Прийнято'), ('Збирається', 'Збирається'), ('Відправлено', 'Відправлено'), ('Готове до видачі', 'Готове до видачі'), ('Відмінено', 'Відмінено')], default='Прийнято', max_length=50, verbose_name='Статус'),
        ),
    ]
